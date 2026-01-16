import os
from spark_session import get_spark_session

def ingest_bronze(DATASET_PATH,BRONZE_PATH):
    """
    Stockage Bronze (données brutes)
    """
    spark = get_spark_session("Ingest Bronze Taxi")

    df = spark.read.parquet(DATASET_PATH)

    os.makedirs(os.path.dirname(BRONZE_PATH), exist_ok=True)

    df.write.mode("overwrite").parquet(BRONZE_PATH)

    print("Données brutes chargées dans la table bronze_taxi")

    spark.stop()

