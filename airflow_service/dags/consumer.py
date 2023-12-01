import requests

from datetime import datetime

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner': 'mp',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0
}

dag = DAG(
    'sr_consumer',
    default_args=default_args,
    description='Run kafka consumer for search_request in app.service',
    schedule_interval='* 1 * * *',
    catchup=False,
    concurrency=1
)


def sr_consume():
    res = requests.get('http://app:8000/consumer')
    result = res.json()
    if result['status'] != 0:
        raise Exception(f"Consumer not started {result['msg']}")


task_1 = PythonOperator(
    task_id='sr_consume',
    python_callable=sr_consume,
    provide_context=True,
    dag=dag,
)