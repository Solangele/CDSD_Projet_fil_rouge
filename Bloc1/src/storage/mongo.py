"""
Module de structuration et d'enrichissement (Pipeline Bronze vers Silver).

Ce script récupère les objets bruts stockés dans le stockage objet MinIO (couche Bronze), applique des règles de nettoyage (filtrage des formats, exclusion des fichiers systèmes), extrait intelligemment les labels d'instruments, calcule la durée audio réelle, et sauvegarde ces documents nettoyés et uniformisés dans MongoDB (couche Silver).
"""


import os
import io
import boto3
import soundfile as sf
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv(dotenv_path="../../.env") 


s3 = boto3.client('s3',
    endpoint_url='http://localhost:9000',
    aws_access_key_id=os.getenv('MINIO_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('MINIO_SECRET_KEY')
)

dbname = os.getenv('MONGO_DBNAME')

mongo_client = MongoClient(
    host='localhost',
    port=27017,
    username=os.getenv('MONGO_USER'),
    password=os.getenv('MONGO_PASSWORD'),
    authSource= 'admin'
)

db = mongo_client[dbname]
collection = db['metadata']

IRMAS_INSTRUMENTS = {
    "cel": "celesta", "cla": "clarinet", "flg": "flute", "gac": "acoustic_guitar",
    "gel": "electric_guitar", "org": "organ", "pia": "piano", "sax": "saxophone",
    "tru": "trumpet", "vln": "violin", "voi": "voice"
}


def extract_instrument_label(bucket_name, file_key, source_name):
    """
    Extrait et normalise le label de l'instrument d'un fichier brut (Bronze).
    
    Cette étape participe à la mise en conformité de la donnée pour la couche Silver en appliquant 3 stratégies successives pour le dataset IRMAS (dossier parent, nom du fichier, ou lecture du fichier texte d'accompagnement).

    Arguments:
        bucket_name (str): Nom du bucket MinIO.
        file_key (str): Chemin/Clé unique du fichier sur le stockage.
        source_name (str): Origine du dataset ("philharmonia_scrap" ou "irmas_dataset").

    Retourne:
        str: Le nom complet de l'instrument normalisé, ou "unknown".
    """

    file_key_lower = file_key.lower()
    
    if source_name == "philharmonia_scrap":
        return file_key.split('/')[0]
        
    elif source_name == "irmas_dataset":
        irmas_codes = list(IRMAS_INSTRUMENTS.keys())
        
        parts = file_key_lower.split('/')
        if len(parts) > 1 and parts[1] in irmas_codes:
            return IRMAS_INSTRUMENTS[parts[1]] 
            
        for code in irmas_codes:
            if f"[{code}]" in file_key_lower or f"_{code}_" in file_key_lower:
                return IRMAS_INSTRUMENTS[code] 
                

        base_path, _ = os.path.splitext(file_key)
        txt_key = base_path + ".txt"
        
        try:
            txt_obj = s3.get_object(Bucket=bucket_name, Key=txt_key)
            txt_content = txt_obj['Body'].read().decode('utf-8').strip().lower()

            for word in txt_content.split():
                clean_word = word.strip()
                if clean_word in irmas_codes:
                    return IRMAS_INSTRUMENTS[clean_word]
                    
        except Exception:
            return "unknown"
                
    return "unknown"




def get_minio_audio_duration(bucket_name, file_key):
    """
    Télécharge l'objet binaire depuis MinIO pour calculer sa durée réelle en secondes.

    Cette fonction charge le contenu binaire en mémoire via un flux io.BytesIO, puis utilise soundfile pour diviser le nombre de frames par la fréquence d'échantillonnage.

    Arguments :
        bucket_name (str) : Le nom du bucket MinIO
        file_key (str) : La clé unique (chemin) du fichier audio. 

    Retourne :
        float : La durée du fichier en secondes, ou None en cas d'erreur de lecture. 
    """
    try:
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        audio_data = response['Body'].read()
        
        with sf.SoundFile(io.BytesIO(audio_data)) as f:
            return len(f) / f.samplerate
    except Exception as e:
        print(f"Impossible de lire la durée de {file_key}: {e}")
        return None




def index_minio_to_mongodb(bucket_name, source_name):
    """
    Parcourt un bucket MinIO, extrait les métadonnées de chaque fichier audio et les pousse dans MongoDb.

    La fonction utilise un paginateur S3 pour traiter les buckets contenant un grand nombre de fichiers. Chaque document inséré contient le nom, le chemin d'accès complet, la taille, la date de modification, le label extrait et la durée audio calculée. 
    La clé d'unicité dans MongoDB est le champ 'minio_path' (Upsert).

    Arguments :
        bucket_name (str) : Le nom du bucket cible à scanner.
        source_name (str) : Identifiant de la source (ex: "philarmonia_scrap").
    
    Retourne : 
        None
    """

    print(f"Indexation du bucket '{bucket_name}' (Source: {source_name})...")
    

    paginator = s3.get_paginator('list_objects_v2')
    count = 0

    for page in paginator.paginate(Bucket=bucket_name):
        if 'Contents' in page:
            for obj in page['Contents']:
                file_key = obj['Key']
                

                if file_key.lower().endswith(('.wav', '.mp3')):
                    try:
                        label = extract_instrument_label(bucket_name, file_key, source_name)

                        duration = get_minio_audio_duration(bucket_name, file_key)

                        metadata = {
                            "filename": os.path.basename(file_key),
                            "minio_path": f"{bucket_name}/{file_key}",
                            "label": label,
                            "source": source_name,
                            "size_bytes": obj['Size'],
                            "duration_seconds": duration, 
                            "last_modified": obj['LastModified']
                        }

                        collection.update_one(
                            {"minio_path": metadata["minio_path"]}, 
                            {"$set": metadata}, 
                            upsert=True
                        )
                        count += 1
                        
                        if count % 500 == 0:
                            print(f"  {count} fichiers indexés...")
                            
                    except Exception as file_error:
                        print(f"Fichier ignoré suite à une erreur sur {file_key}: {file_error}")
                        continue
    
    
    print(f"{count} documents indexés pour {source_name}.")

if __name__ == "__main__":
    index_minio_to_mongodb("philharmonia", "philharmonia_scrap")
    index_minio_to_mongodb("irmas", "irmas_dataset")