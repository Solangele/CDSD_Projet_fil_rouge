"""
Pipeline principal d'orchestration de données (Orchestrateur End-to-End)

Ce script centralise et exécute séquentiellement toutes les étapes du projet :
1. Extraction (Scraping) : Récupération des données source.
2. Ingestion (Landing/Bronze) : Téléversement du vrac local vers le Data Lake Minio.
3. Enrichissement (Silver) : Indexation, nettoyage et calculs de métadonnées dans MongoDB.
4. Structuration (Gold) : Migration relationnelle et mise en conformité analytique dans PostgreSQL.
"""

import os
from dotenv import load_dotenv
from src.ingestion.scrap import etl_philharmonia_to_disk
from src.storage.minio import upload_folder_to_minio
from src.storage.mongo import index_minio_to_mongodb
from src.storage.postgres import init_postgres_schema, load_silver_to_gold

# 1. Chargement du .env (avec ton nouveau chemin propre)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
load_dotenv(dotenv_path=os.path.join(project_root, '.env'))

def main():
    """
    Pilote l'exécution séquentielle du pipeline de données. 

    Vérifie l'état de données locales avant de lancer le scraping, puis coordonne les transferts entre les différentes bases de stockage. 
    Chaque sous-fonction appelée encapsule sa propre gestion des erreurs. 

    Retourne :
        None
    """

    print("--- DÉMARRAGE DU PIPELINE GLOBAL ---")

    # ÉTAPE 1 : SCRAPING (Local)
    if not os.path.exists("data/scrap/philharmonia"):
        print("Phase 1 : Scraping Philharmonia...")
        etl_philharmonia_to_disk()
    else:
        print("Phase 1 : Données locales déjà présentes.")

    # ÉTAPE 2 : STOCKAGE (MinIO)
    print("Phase 2 : Upload vers le Data Lake (MinIO)...")
    upload_folder_to_minio("data/scrap/philharmonia", "philharmonia")
    upload_folder_to_minio("data/IRMAS", "irmas")

    # ÉTAPE 3 : INDEXATION (MongoDB)
    print("Phase 3 : Création du catalogue (MongoDB)...")
    index_minio_to_mongodb("philharmonia", "philharmonia_scrap")
    index_minio_to_mongodb("irmas", "irmas_dataset")

    # ÉTAPE 4 : STRUCTURATION ET RELATIONS (PostgreSQL - Gold)
    print("Phase 4 : Structuration relationnelle (PostgreSQL Gold)...")
    init_postgres_schema()
    load_silver_to_gold()

    print("--- TOUT EST PRÊT ! ---")

if __name__ == "__main__":
    main()