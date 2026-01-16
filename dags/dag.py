from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import os

# Import des fonctions ETL
from ML.Scripts.Load_data import load_data
from ML.Scripts.ingest_bronze import ingest_bronze
from ML.Scripts.silver_etl import etl_pipeline

# ---------------- Configuration ----------------

DAG_ID = "taxi_etl_pipeline"

DATASET_PATH = "/opt/airflow/data/dataset.parquet"
BRONZE_PATH = "/opt/airflow/data/bronze/bronze_taxi.parquet"

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2026, 1, 3),
    "retries": 1,
}

# ---------------- DAG ----------------

with DAG(
    dag_id=DAG_ID,
    default_args=default_args,
    description="Pipeline Taxi : Load → Bronze → Silver → PostgreSQL",
    schedule_interval=None,
    catchup=False,
) as dag:

    # -------- Tâche 0 : Vérification dataset --------


    load_data_task = PythonOperator(
        task_id="load_data",
        python_callable=load_data,
        op_kwargs={"DATA_PATH": DATASET_PATH}
    )

    # -------- Tâche 1 : Ingest Bronze --------
    ingest_bronze_task = PythonOperator(
        task_id="ingest_bronze",
        python_callable=ingest_bronze,
        op_kwargs={
            "DATA_PATH": DATASET_PATH,
            "BRONZE_TAXI_PATH": BRONZE_PATH
        }
    )

    # -------- Tâche 2 : Silver + PostgreSQL --------
    silver_to_postgres_task = PythonOperator(
        task_id="silver_to_postgres",
        python_callable=etl_pipeline,
        op_kwargs={
            "BRONZE_TAXI_PATH": BRONZE_PATH
        }
    )


    load_data_task >> ingest_bronze_task >> silver_to_postgres_task
