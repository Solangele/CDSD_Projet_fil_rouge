"""
API Web de déploiement et routage acoustique (Bloc 5)

Ce module Flask encapsule le modèle de Deep Learning (CNN) entrapiné au Bloc 4.
Il fournit une interface web et un endpoint REST permettant de charger un fichier audio brut, de le transformer en Mel-Spectrogramme à la volée, et de router le signal vers l'une des 7 familles d'instruments cibles avec une gestion de seuil de confiance (KPI).

Prérequis :
    - Le fichier 'model_cnn_optimal.keras' doit être présent dans le même dossier
    - Librairies : Flask, librosa, numpy, tensorflow, werkzeug

Endpoints :
    - GET / : interface web utilisateur (IHM)
    - POST /predict : Endpoint de prédiction (reçoit le fichier audio et renvoie un JSON).
"""


import os
import numpy as np
import librosa
import tensorflow as tf
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, render_template_string, render_template

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

if not os.path.exists(TEMPLATE_DIR):
    TEMPLATE_DIR = os.path.join(BASE_DIR, 'Bloc5', 'templates')

app = Flask(__name__, template_folder=TEMPLATE_DIR)
app.json.ensure_ascii = False


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(SCRIPT_DIR, "model_cnn_optimal.h5")


if os.path.exists(MODEL_PATH):
    print(f"Récupération du modèle optimal : {MODEL_PATH}")
    model = tf.keras.models.load_model(MODEL_PATH, compile=False)
else:
    raise FileNotFoundError(f"Le modèle '{MODEL_PATH}' est introuvable dans le dossier Bloc5.")


RAW_CLASSES_26 = [
    "acoustic_guitar", "banjo", "bass clarinet", "bassoon", 
    "celesta", "cello", "clarinet", "contrabassoon", 
    "cor anglais", "double bass", "electric_guitar", "flute", 
    "french horn", "guitar", "mandolin", "oboe", 
    "organ", "percussion", "piano", "saxophone", 
    "trombone", "trumpet", "tuba", "viola", 
    "violin", "voice"
]


FAMILY_7 = [
    "Famille des Cordes Frottées",  
    "Famille des Cordes Pincées",     
    "Orgues & Claviers Anciens",
    "Percussions",
    "Pianos & Claviers Frappés",
    "Instruments à Vent & Cuivres",
    "Chant & Voix Humaines" 
]

def process_and_predict(audio_path):
    """
  Pipeline d'inférence complet : Transforme un signal audio en descripteur visuel (Mel-Spectrogramme) et applique un routage multiniveau adaptatif. 

  Logique algorithmique du routage :
    - Si le modèle possède 7 neurones de sortie : cartographie directe vers les familles macro-métiers (FAMILY_7).
    - Si le modèle possède une granularité fina (ex : 26 sorties) : Classification au niveau de l'instrument (RAW_CLASSES_26) puis agrégation déductive via un arbre de décidion 'if/elif' pour garantir le format pivot à 7 familles. 

    Arguments : 
        audio_path (str) : chemin d'accès local vers le fichier audio à analyser.

    Retourne : 
        Un tuple contenant 2 éléments : 
            - str : le nom de la famille d'instruments identifié (parmi les 7 familles officielles).
            - float : le score de confiance associé à la prédiction, exprimé en pourcentage [0.0 ; 100.0]
    """
    y, sr = librosa.load(audio_path, sr=22050, duration=3.0)
    mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
    mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
    
    if mel_spec_db.shape[1] < 128:
        mel_spec_db = np.pad(mel_spec_db, ((0, 0), (0, 128 - mel_spec_db.shape[1])), mode='constant')
    else:
        mel_spec_db = mel_spec_db[:, :128]
        
    min_val = mel_spec_db.min()
    max_val = mel_spec_db.max()
    if max_val - min_val != 0:
        mel_spec_db = (mel_spec_db - min_val) / (max_val - min_val)
    else:
        mel_spec_db = np.zeros_like(mel_spec_db)

    input_tensor = np.expand_dims(mel_spec_db, axis=(0, -1))
    

    predictions = model.predict(input_tensor)[0]
    model_output_nodes = len(predictions)
    predicted_index = np.argmax(predictions)
    confidence_score = float(predictions[predicted_index]) * 100 
    

    if model_output_nodes == 7:
        return FAMILY_7[predicted_index], confidence_score
        

    else:
        raw_instrument_name = RAW_CLASSES_26[predicted_index] if predicted_index < len(RAW_CLASSES_26) else "autre"
        

        if raw_instrument_name in ["organ"]:
            return FAMILY_7[2], confidence_score
        elif raw_instrument_name in ["banjo", "guitar", "mandolin", "electric_guitar", "acoustic_guitar"]:
            return FAMILY_7[1], confidence_score
        elif raw_instrument_name in ["voice"]:
            return FAMILY_7[6], confidence_score
        elif raw_instrument_name in ["bassoon", "cello", "contrabassoon", "double bass", "viola", "violin"]:
            return FAMILY_7[0], confidence_score
        elif raw_instrument_name in ["piano", "celesta"]:
            return FAMILY_7[4], confidence_score
        elif raw_instrument_name in ["percussion"]:
            return FAMILY_7[3], confidence_score
        else:
            return FAMILY_7[5], confidence_score


HTML_INTERFACE = """
<!DOCTYPE html>
<html>
<head>
    <title>IA Audio - Routage Securisé</title>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; margin: 0; background-color: #f4f6f9; display: flex; align-items: center; justify-content: center; height: 100vh; }
        .card { background: white; padding: 40px; border-radius: 12px; box-shadow: 0 8px 25px rgba(0,0,0,0.05); max-width: 550px; width: 100%; text-align: center; }
        h2 { color: #2c3e50; margin: 0 0 10px 0; font-size: 24px; }
        p { color: #7f8c8d; margin-bottom: 30px; font-size: 14px; }
        .file-input { margin: 20px 0; padding: 15px; border: 2px dashed #3498db; border-radius: 8px; background: #f8fafc; width: 85%; font-size: 14px; }
        button { background: #3498db; color: white; border: none; padding: 14px 30px; border-radius: 6px; font-size: 16px; font-weight: bold; cursor: pointer; transition: background 0.2s; }
        button:hover { background: #2980b9; }
        .footer { margin-top: 25px; font-size: 11px; color: #bdc3c7; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🎵 Tri et Routage Audio Intel-Safe</h2>
        <p>Objectif 7 Familles</p>
        <hr style="border: 0; border-top: 1px solid #edf2f7; margin-bottom: 20px;">
        <form action="/predict" method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept=".wav,.mp3" class="file-input" required><br>
            <button type="submit">Analyser et Router</button>
        </form>
        <div class="footer">Démonstrateur de Production Auto-Synchronisé</div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_INTERFACE)

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'erreur': 'Aucun fichier détecté'}), 400
    
    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        return jsonify({'erreur': 'Aucun fichier sélectionné'}), 400
    

    filename_secured = secure_filename(uploaded_file.filename)
    temporary_path = os.path.join(SCRIPT_DIR, filename_secured)
    uploaded_file.save(temporary_path)
    
    try:
        detected_family, confidence = process_and_predict(temporary_path)
        statut = "Succès"
        

        SEUIL_CONFIDENCE_KPI = 70.0 
        
        if confidence < SEUIL_CONFIDENCE_KPI:
            routing_status = "Alerte : Niveau de confiance insuffisant (< 70%)"
            industrial_action = "Routage suspendu - Envoi immédiat au bac de révision manuel (Secrétariat)"
        else:
            routing_status = "Validé"
            industrial_action = f"Routage automatique vers le répertoire industriel : {detected_family}"
            
    except Exception as e:
        detected_family = "Erreur de classification"
        confidence = 0.0
        statut = f"Erreur technique : {str(e)}"
        routing_status = "Échec technique"
        industrial_action = "Aucune action - Fichier corrompu ou illisible"
        
    finally:
        if os.path.exists(temporary_path):
            os.remove(temporary_path)

    result = {
        'statut': statut,
                'analyzed_file': filename_secured,
                'identified_instrument_family': detected_family,
                'global_confidence_score': f"{confidence:.2f}%",
                'confidence_value': round(confidence, 2),
                'business_routing_status': routing_status,
                'industrial_deployment_action': industrial_action
    }
            
    return render_template('result.html', data = result)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)