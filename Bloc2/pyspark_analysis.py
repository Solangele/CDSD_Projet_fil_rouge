"""
Module d'analyse Big Data distribuée via PySpark.

Ce script se connecte à un cluster Spark autonome (Standalone Docker), aspire les données de la couche Gold de PostgreSQL via une passerelle JDBC, et exécute un plan d'agrégation statistique lours entièrement parallélisé sur les noeuds du cluster (Workers).
"""

import os
import time
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

db_name = os.getenv('POSTGRES_DB')
db_user = os.getenv('POSTGRES_USER')
db_pass = os.getenv('POSTGRES_PASSWORD')

if not db_name or not db_user or not db_pass:
    print("Erreur : Impossible de charger les variables PostgreSQL depuis le .env")
    exit(1)

print("Configuration de l'environnement chargée avec succès.")


print("Connexion au cluster Spark (Docker) en cours...")
spark = SparkSession.builder \
    .appName("AudioProject_BigData_Analysis") \
    .master("spark://spark-master:7077") \
    .config("spark.jars.packages", "org.postgresql:postgresql:42.7.3") \
    .getOrCreate()


jdbc_url = f"jdbc:postgresql://pfr-postgres:5432/{db_name}"
connection_properties = {
    "user": db_user,
    "password": db_pass,
    "driver": "org.postgresql.Driver"
}


query_table = """
(SELECT t.filename, t.duration_seconds, t.size_bytes, t.source_dataset, i.label_name as instrument 
 FROM audio_tracks t 
 JOIN instruments i ON t.instrument_id = i.id) as audio_gold_data
"""

print("Chargement distribué des données depuis PostgreSQL Gold...")
try:
    spark_df = spark.read.jdbc(
        url=jdbc_url, 
        table=query_table, 
        properties=connection_properties
    )
except Exception as e:
    print(f"❌ Erreur lors de la lecture JDBC : {e}")
    print("Vérifie que ta base PostgreSQL est bien allumée et contient des données.")
    spark.stop()
    exit(1)


print("Lancement de l'analyse statistique distribuée sur le cluster...")
start_time = time.time()


statistiques_multivariees = spark_df.groupBy("instrument", "source_dataset") \
    .agg(
        F.count("filename").alias("total_pistes"),
        F.round(F.mean("duration_seconds"), 2).alias("duree_moyenne_sec"),
        F.round(F.mean("size_bytes") / 1024 / 1024, 2).alias("taille_moyenne_mo"),
        F.min("duration_seconds").alias("duree_min"),
        F.max("duration_seconds").alias("duree_max")
    ) \
    .orderBy("instrument")


statistiques_multivariees.show(40, truncate=False)

execution_time = time.time() - start_time
print(f"Temps de calcul parallélisé avec Spark : {execution_time:.4f} secondes")


spark.stop()
print("Session Spark clôturée.")