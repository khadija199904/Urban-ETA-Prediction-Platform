from pyspark.sql import SparkSession
from pyspark.sql.functions import col, unix_timestamp, hour, dayofweek, month, mean, stddev, abs
from database import engine


# -------------------------------- Initialiser Spark ---------------------------

spark = SparkSession.builder \
    .appName("ETL Bronze → Silver") \
    .enableHiveSupport() \
    .getOrCreate()


# --------------------- Chargerement les données -------------------------------

path = "data/dataset.parquet"

df = spark.read.parquet(path)

# Créer la base Bronze si elle n'existe pas
spark.sql("CREATE DATABASE IF NOT EXISTS bronze")
df.write.format("parquet").mode("overwrite").saveAsTable("bronze.bronze_taxi")

print("Données brutes chargées dans la base Bronze")

# ------------------ Nettoyage des données → Silver --------------------------

silver_df = spark.table("bronze.bronze_taxi")

# Supprimer doublons
silver_df = silver_df.distinct()

# Supprimer valeurs manquantes
silver_df = silver_df.dropna()

# Filtrer trajets aberrants
silver_df = silver_df.filter((col("trip_distance") > 0) & (col("trip_distance") <= 200))
silver_df = silver_df.filter(col("passenger_count") > 0)

# Calculer la durée du trajet en minutes (cible)
silver_df = silver_df.withColumn(
    "trip_duree",
    (unix_timestamp(col("tpep_dropoff_datetime")) - unix_timestamp(col("tpep_pickup_datetime"))) / 60
)


# --------------------------Feature Engineering ------------------------------------


# Convertir en timestamp
silver_df = silver_df.withColumn("tpep_pickup_datetime", col("tpep_pickup_datetime").cast("timestamp")) \
                     .withColumn("tpep_dropoff_datetime", col("tpep_dropoff_datetime").cast("timestamp"))

# Extraire features temporelles
silver_df = silver_df.withColumn("pickup_hour", hour(col("tpep_pickup_datetime"))) \
                     .withColumn("day_of_week", dayofweek(col("tpep_pickup_datetime"))) \
                     .withColumn("month", month(col("tpep_pickup_datetime")))


# ----------------------------- Supprimer outliers (Z-score) --------------------------------

numeric_cols = [
    "passenger_count",
    "trip_distance", 
    "PULocationID",
    "DOLocationID",
    "fare_amount",
    "extra",
    "mta_tax",
    "tip_amount",
    "tolls_amount",
    "improvement_surcharge",
    "total_amount",
    "congestion_surcharge",
    "Airport_fee",
    "cbd_congestion_fee",
    "trip_duree"  
]

silver_df_clean = silver_df

for c in numeric_cols:
    stats = silver_df_clean.select(mean(col(c)).alias("mean"), stddev(col(c)).alias("stddev")).collect()[0]
    mean_val, std_val = stats["mean"], stats["stddev"]
    silver_df_clean = silver_df_clean.withColumn(f"z_{c}", (col(c) - mean_val) / std_val)

for c in numeric_cols:
    silver_df_clean = silver_df_clean.filter(abs(col(f"z_{c}")) <= 3)

# Supprimer colonnes Z-score temporaires
silver_df_clean = silver_df_clean.drop(*[f"z_{c}" for c in numeric_cols])

# Supprimer RatecodeID invalides
silver_df_clean = silver_df_clean.filter(
    col("RatecodeID").isin([1, 2, 3, 4, 5, 6])
 ).filter(
    col("trip_duree") > 1
)



# Supprimer colonnes inutiles
cols_to_drop = ["VendorID","tpep_pickup_datetime","tpep_dropoff_datetime","store_and_fwd_flag",
                "passenger_count","extra","tolls_amount","congestion_surcharge","Airport_fee",
                "PULocationID","DOLocationID","mta_tax","improvement_surcharge"]
silver_df_clean = silver_df_clean.drop(*cols_to_drop)


# --------------------Stockage dans la base Silver -------------------------------

spark.sql("CREATE DATABASE IF NOT EXISTS silver")
silver_df_clean.write.format("parquet").mode("overwrite").saveAsTable("silver.silver_taxi")

print("Données Silver stockées ")


#-------------------- Export Silver vers PostgreSQL ----------------------


# Convertir en Pandas
df_p = silver_df_clean.toPandas()


table_name = "silver_taxi"
df_p.to_sql(table_name, engine, if_exists="replace", index=False)

print(f" Données stockées avec succès dans PostgreSQL table '{table_name}' ")
