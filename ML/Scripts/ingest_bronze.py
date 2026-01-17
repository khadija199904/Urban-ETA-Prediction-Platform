import os
from spark_session import get_spark_session

def ingest_bronze(DATA_PATH,BRONZE_TAXI_PATH):
    """
    Stockage Bronze (données brutes)
    """
    spark = get_spark_session("Ingest Bronze Taxi")

    df = spark.read.parquet(DATA_PATH)

    os.makedirs(os.path.dirname(BRONZE_TAXI_PATH), exist_ok=True)

    df.write.mode("overwrite").parquet(BRONZE_TAXI_PATH)

    print("Données brutes chargées dans la table bronze_taxi")

    spark.stop()

