# test_preprocessing_simple.py
import pytest
from pyspark.sql import SparkSession
from pyspark.sql import Row
from ML.Scripts.silver_etl import clean_basic ,feature_engineering

# Fixture Spark
@pytest.fixture(scope="session")
def spark():
    spark = SparkSession.builder \
        .master("local[1]") \
        .appName("pytest-spark-simple") \
        .getOrCreate()
    yield spark
    spark.stop()

# ---------------- Fixture DataFrame factice ----------------
@pytest.fixture
def sample_df(spark):
   data = [
    (1, "khadija", 10, 2, "2026-01-17 10:00:00", "2026-01-17 10:30:00"),
    (2, "Nada", 0, 1, "2026-01-17 12:00:00", "2026-01-17 12:45:00"),    # distance invalide
    (3, "Mery", 5, -2, "2026-01-17 14:00:00", "2026-01-17 14:15:00") # passenger_count invalide
     ]

   columns = ["id", "name", "trip_distance", "passenger_count", "tpep_pickup_datetime", "tpep_dropoff_datetime"]
   sample_df = spark.createDataFrame(data, columns)
   return sample_df



def test_clean_basic(sample_df):

    assert sample_df is not None

    df_clean = clean_basic(sample_df)
    # Après le filtrage des trajets à distance invalide et des passenger_count incorrects,
    # une seule ligne valide subsiste dans le DataFrame.
    assert df_clean.count() == 1
    
    # verifier la colonne trip_duree existe
    assert "trip_duree" in df_clean.columns

# ---------------- Test feature_engineering ----------------
def test_feature_engineering(sample_df):
    
    df_feat = feature_engineering(sample_df)
    
    # Vérifie que les colonnes temporelles existent
    cols = df_feat.columns
    assert "pickup_hour" in cols
    assert "day_of_week" in cols
    assert "month" in cols
    
