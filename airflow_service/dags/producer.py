import requests

from datetime import datetime
from datetime import timedelta

from airflow import DAG
from airflow.operators.python_operator import PythonOperator


default_args = {
    'owner': 'mp',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'sr_producer',
    default_args=default_args,
    description='Run kafka producer for search_request in app.service',
    schedule_interval='* 1 * * *',
    catchup=False,
    concurrency=1
)


def sr_produce():
    res = requests.get('http://app:8000/producer')
    result = res.json()
    if result['status'] != 0:
        raise Exception(f"Producer not started {result['msg']}")


task_1 = PythonOperator(
    task_id='sr_produce',
    python_callable=sr_produce,
    provide_context=True,
    dag=dag,
)
