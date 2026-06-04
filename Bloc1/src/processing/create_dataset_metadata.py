"""
Module de génération de métadonnées pour le dataset IRMAS.

Ce script parcourt l'arborescence des fichiers audio d'entraînement IRMAS, extrait les étiquettes (labels) à partir des noms de dossiers, et génère un fichier CSV structuré prêt à être utilisé pour l'entraînement d'un modèle. 
"""


import os
import pandas as pd

def generate_irmas_csv(data_path, output_filename="metadata_irmas.csv"):
    """
    Parcourt un dossier contenant le dataset IRMAS et génère un fichier CSV de métadonnée.

    Structure attendue du dossier cible :
    data/
    └── IRMAS-{type}/
        └──[fichier.wav]

    Arguments :
        data_path (str): Le chemin vers le dossier racine du dataset (ex: "data/IRMAS-TrainigData").
        output_filename (str, optionnel) : Le nom du fichier de sortie.
    
    Retourne :
        None : La fonction sauvegarde directement le fichier CSV sur le disque. 

    """

    data_list = []
    
    for root, dirs, files in os.walk(data_path):
        for file in files:
            if file.endswith(".wav"):
                label = os.path.basename(root)
                file_path = os.path.join(root, file)
                
                data_list.append({
                    "file_path": file_path,
                    "label": label,
                    "instrument_full": label_to_name(label)
                })
    

    df = pd.DataFrame(data_list)
    
    df.to_csv(output_filename, index=False)
    print(f"✅ Terminé ! {len(df)} fichiers indexés dans {output_filename}")

def label_to_name(label):
    """
    Convertit un code court à 3 lettres du jeu de données IRMAS en son nom complet en français.

    Cette fonction utilitaire permet de traduire les abréviations techniques utilisées dans le jeu de données audio en labels clairs et compréhensibles pour l'interface utilisateur. 
    Elle intègre une gesion de classe (majuscules/minuscules) ainsi qu'un mécanisme de secours sécurisé. 

    Argument : 
        label (str) : le code d'instrument à 3 caractères issu du dataset

    Retourne :
        str : le nom complet de l'instrument en français. Renvoie "Inconnu" si le code fourni n'est pas répertorié dans le dictionnaire. 
    """
    mapping = {
        "cel": "Violoncelle",
        "cla": "Clarinette",
        "flt": "Flûte",
        "gac": "Guitare Acoustique",
        "gel": "Guitare Électrique",
        "org": "Orgue",
        "pia": "Piano",
        "sax": "Saxophone",
        "tru": "Trompette",
        "vio": "Violon",
        "voi": "Voix"
    }
    return mapping.get(label.lower(), "Inconnu")


generate_irmas_csv("data/IRMAS-TrainingData")