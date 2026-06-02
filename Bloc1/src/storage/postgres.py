"""
Module de migration et de structuration des données (Pipeline Silver vers Gold).

Ce script se charge de récupérer les documents de métadonnées brut depuis MongoDB (couche Silver), de normaliser et valider les relations (tables de faits et de dimensions), puis de charger ces informations de façon structurée dans PostgreSQL (couche Gold).
"""

import os
import psycopg2
from pymongo import MongoClient
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir)) 
load_dotenv(dotenv_path=os.path.join(project_root, '.env'))


def get_postgres_connection():
    """
    Initialise et retourne une connexion active vers la base de données PostgreSQL.

    Les identifiants sensibles sont récupérés depuis les variables d'environnement. 

    Retourne :
        psycopg2.extensions.connection : Objet de connexion à la base de données. 
    """

    return psycopg2.connect(
        host= "localhost",
        port= "5432",
        database= "datapulse_db",
        user= os.getenv("POSTGRES_USER"),
        password= os.getenv("POSTGRES_PASSWORD")
    )


def init_postgres_schema():
    """ 
    Initialise le schéma relationnel de la couche Gold dans PostgreSQL.

    Créé les deux tables principelles si elles n'existent pas encore : 
    1. 'instruments' (Table de dimension) : Stocke de manière unique les noms d'instruments.
    2. 'audio_tracks' (Table de faits) : Contient les métadonnées techniques de chaque piste et est liée à la table instruments via une clé étrangère (Foreign Key).

    Retourne :
        None
    """
    commands = (
        """
        CREATE TABLE IF NOT EXISTS instruments (
            id SERIAL PRIMARY KEY,
            label_name VARCHAR(100) UNIQUE NOT NULL
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS audio_tracks (
            id SERIAL PRIMARY KEY,
            filename VARCHAR(255) NOT NULL,
            minio_path VARCHAR(550) UNIQUE NOT NULL,
            instrument_id INT references instruments(id) ON DELETE CASCADE,
            source_dataset VARCHAR(100) NOT NULL,
            size_bytes BIGINT,
            duration_seconds REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn = None
    try:
        conn = get_postgres_connection()
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        cur.close()
        conn.commit()
        print("Schéma PostgreSQL (Gold) initialisé avec succès !!")
    except Exception as error:
        print(f"Erreur lors de l'initialisation de SQL : {error}")
    finally:
        if conn is not None:
            conn.close()


def load_silver_to_gold():
    """
    Aspire les données de MongoDB (Silver) et les injecte de façon relationnelle dans PostgreSQL (Gold).

    Le processus suit la logique suivante pour chaque document MongoDB :
    1. Nettoyage du label d'instrument.
    2. Insertion de l'instrument dans la table de dimension. Si l'instrument existe déjà, la contrainte UNIQUE  intercepte le doublon (ON CONFLICT) et on récupère l'identifiant existant.
    3. Insertion des métadonnées de la piste audio dans la table de faits, liée à l'instrument_id.
    4. En cas d'erreur sur une piste, un mécanisme de 'rollback sécurise la transaction courante pour passer proprement au document suivant. 

    Retourne :
        None
    """
    print("Début de la transition Silver -> Gold")

    mongo_client = MongoClient(
        host= 'localhost',
        port= 27017,
        username= os.getenv('MONGO_USER'),
        password= os.getenv('MONGO_PASSWORD')
    )

    db_name = os.getenv('MONGO_DBNAME')
    db = mongo_client[db_name]
    mongo_docs = db.metadata.find()

    conn = get_postgres_connection()
    cur = conn.cursor()

    tracks_inserted = 0

    for doc in mongo_docs:
        label = doc.get('label', 'unknown').lower().strip()

        cur.execute(
            """
            INSERT INTO instruments (label_name) 
            VALUES (%s) 
            ON CONFLICT (label_name) DO NOTHING RETURNING id;
            """
            ,
            (label,)
        )
        res = cur.fetchone()

        if res :
            instrument_id = res[0]
        else :
            cur.execute(
                "SELECT ID FROM instruments WHERE label_name = %s",
                (label,)
                )
            instrument_id = cur.fetchone()[0]

        try:
            cur.execute(
                """
                INSERT INTO audio_tracks(filename, minio_path, instrument_id, source_dataset, size_bytes, duration_seconds)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (minio_path) DO NOTHING;
                """,
                (doc['filename'], doc['minio_path'], instrument_id, doc['source'], doc['size_bytes'], doc.get('duration_seconds'))
            )   
            tracks_inserted += cur.rowcount
            
        except Exception as e:
            print(f"Erreur insertion piste {doc['filename']} : {e}")
            conn.rollback()
            continue

    conn.commit()
    cur.close()
    conn.close()
    print(f"Transition terminée. {tracks_inserted} nouvelles pistes structurées dans PostgreSQL Gold.")

if __name__ == "__main__":
    init_postgres_schema()
    load_silver_to_gold()