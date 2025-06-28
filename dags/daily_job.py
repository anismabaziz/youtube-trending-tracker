from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Add project root to Python path
sys.path.append('/opt/airflow/scripts')

from script import main

default_args = {
    'owner': 'anis',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='daily_youtube_fetch',
    default_args=default_args,
    description='Fetch and save trending YouTube videos daily',
    schedule_interval='0 8 * * *',  # Every day at 8 AM
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:
    run_script = PythonOperator(
        task_id='run_fetch_and_save',
        python_callable=main,
    )
