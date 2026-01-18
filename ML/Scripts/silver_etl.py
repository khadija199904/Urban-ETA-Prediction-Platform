from pyspark.sql.functions import col, unix_timestamp, hour, dayofweek, month,mean, stddev, abs
from .spark_session import get_spark_session
from api.database import engine


# ------------------- 1. Lecture des données Bronze -------------------

def read_bronze_data(spark, path):
    """Lire le dataset Bronze depuis parquet"""
    print(f"Lecture des données depuis : {path}")
    return spark.read.parquet(path)


# ------------------- 2. Nettoyage de base  -------------------

def clean_basic(df):
    
    # Supprimer doublons et valeurs manquantes
    df_clean = df.distinct().dropna()

    # Filtrer trajets aberrants
    df_clean = df_clean.filter((col("trip_distance") > 0) & (col("trip_distance") <= 200))
    df_clean = df_clean.filter(col("passenger_count") > 0)

    # Calculer la durée du trajet en minutes
    df_clean = df_clean.withColumn(
        "trip_duree",
        (unix_timestamp(col("tpep_dropoff_datetime")) - unix_timestamp(col("tpep_pickup_datetime"))) / 60
    )

    # filtrer Durée > 0 minutes
    df_clean = df_clean.filter( (col("trip_duree") > 0) )

    return df_clean


# ------------------- 3. Feature Engineering -------------------

def feature_engineering(df):

    """ Extraire features Temporelles """
    # Convertir en timestamp
    df = df.withColumn("tpep_pickup_datetime", col("tpep_pickup_datetime").cast("timestamp")) \
           .withColumn("tpep_dropoff_datetime", col("tpep_dropoff_datetime").cast("timestamp"))
    

    df = df.withColumn("pickup_hour", hour(col("tpep_pickup_datetime"))) \
           .withColumn("day_of_week", dayofweek(col("tpep_pickup_datetime"))) \
           .withColumn("month", month(col("tpep_pickup_datetime")))
    return df

def clean_after_analysis(df, numeric_cols) :

    """
    Supprimer outliers (Z-score) et colonnes fortement corrélées
    - numeric_cols : colonnes numériques pour Z-score
    - corr_threshold : seuil pour supprimer colonnes fortement corrélées
    """
    # --- Supprimer outliers (Z-score) ---
    df_clean = df
    for c in numeric_cols:
        stats = df_clean.select(mean(col(c)).alias("mean"), stddev(col(c)).alias("stddev")).collect()[0]
        mean_val, std_val = stats["mean"], stats["stddev"]
        df_clean = df_clean.withColumn(f"z_{c}", (col(c) - mean_val) / std_val)

    for c in numeric_cols:
        df_clean = df_clean.filter(abs(col(f"z_{c}")) <= 3)
    df_clean = df_clean.drop(*[f"z_{c}" for c in numeric_cols])

    # Supprimer RatecodeID invalides et duree tres faible
    df_clean = df_clean.filter(
        col("RatecodeID").isin([1, 2, 3, 4, 5, 6])
    ).filter(
        col("trip_duree") > 1
    )
    
    # Supprimer colonnes inutiles
    cols_to_drop = ["VendorID","tpep_pickup_datetime","tpep_dropoff_datetime","store_and_fwd_flag",
                    "passenger_count","extra","tolls_amount","congestion_surcharge","Airport_fee",
                    "PULocationID","DOLocationID","mta_tax","improvement_surcharge"]
    df_clean = df_clean.drop(*cols_to_drop)

    
    return df_clean
    

# ------------------- 5. Export vers PostgreSQL -------------------

def export_to_postgres(df):

    """Exporter le DataFrame silver  vers PostgreSQL"""
    df_p = df.toPandas()
    table_name = "silver_taxi"
    df_p.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"Table '{table_name}' exportée vers PostgreSQL")



def etl_pipeline(BRONZE_TAXI_PATH: str):

    """Pipeline complet ETL Silver"""
    spark = get_spark_session("Silver Taxi Processing")

    # 1. Lecture des données
    df = read_bronze_data(spark, BRONZE_TAXI_PATH)

    # 2. Nettoyage de base
    df = clean_basic(df)
    

    # 3. Feature engineering
    df = feature_engineering(df)

    # 4. Nettoyage avancé après exploration
    numeric_cols = [
        "passenger_count","trip_distance","PULocationID","DOLocationID","fare_amount",
        "extra","mta_tax","tip_amount","tolls_amount","improvement_surcharge",
        "total_amount","congestion_surcharge","Airport_fee","cbd_congestion_fee","trip_duree"
    ]
    df = clean_after_analysis(df, numeric_cols)

    # 5. Export vers PostgreSQL
    export_to_postgres(df)

    spark.stop()

   
    



