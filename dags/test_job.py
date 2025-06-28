from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def say_hello():
    print("👋 Hello from Airflow!")

default_args = {
    'owner': 'test',
    'retries': 0,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='test_hello_airflow',
    default_args=default_args,
    description='A simple test DAG',
    schedule_interval=None,  # Only run manually
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:
    hello_task = PythonOperator(
        task_id='say_hello_task',
        python_callable=say_hello,
    )
