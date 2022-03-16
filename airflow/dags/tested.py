import os
import logging
from datetime import date, datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}

def print_dupa():
    print('dupa')

with DAG(
    dag_id="test",
    schedule_interval="0 23 * * *",
    start_date=datetime(2022, 1, 1),
    default_args=default_args,
    catchup=True,
    max_active_runs=10,
    tags=['skibooj'],
)as dag:

        t1  = BashOperator(
            task_id="pierwsze",
            bash_command=f"echo dzien dobry"
        )

        t2 = BashOperator(
            task_id="drugi",
            bash_command=f"echo dobry wieczor"
        )
        t1 >> t2