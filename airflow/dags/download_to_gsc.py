import os
import logging
import requests
from pathlib import Path
import pandas as pd
from datetime import date, datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import openpyxl
import pyspark
from google.cloud import storage


default_args = {
    "owner": "airflow",
    "start_date": days_ago(15),
    "depends_on_past": False,
    "retries": 1,
}
PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")
TODAY_DATE = '{{ execution_date.strftime(\'%d-%m-%Y\') }}'
SEC_TYPE = '10'
PATH_TO_LOCAL_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
PATH_TEMPLATE_DOWNLOAD = f"{PATH_TO_LOCAL_HOME}/{TODAY_DATE}.xls"
PATH_TEMPLATE_PARQUET =f"{PATH_TO_LOCAL_HOME}/{TODAY_DATE}.parquet"
PATH_TEMPLATE_GSC = f"stock/wse/shares/{{{{ execution_date.strftime(\'%Y\') }}}}/{{{{ execution_date.strftime(\'%m\') }}}}/wse_shares_{TODAY_DATE}.parquet"

def gpw_download(date,security_type,path_template) -> None:
   
    base_url ='https://www.gpw.pl/archiwum-notowan'
    url_params = {'fetch':'1',
                'type':security_type,
                'date':date}

    resp = requests.get(base_url, params=url_params, verify=False)
    Path(path_template).parents[0].mkdir(parents=True, exist_ok=True)
    
    with Path(path_template).open(mode ='wb') as output:
        output.write(resp.content)


def format_to_parquet(src_file,final_dir):
    df = pd.read_excel(src_file)
    df.to_parquet(final_dir)

def upload_to_gcs(bucket, object_name, local_file):
    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)



with DAG(
    dag_id="download_to_gsc_dag",
    schedule_interval="0 18 * * 1-5",
    default_args=default_args,
    catchup=True,
    max_active_runs=10,
    tags=['wse'],
) as dag:
    

    dowload_data_wse_task = PythonOperator(
        task_id="dowload_data_wse_task",
        python_callable=gpw_download,
        op_kwargs={
            "date":TODAY_DATE,
            "security_type":SEC_TYPE,
            "path_template":PATH_TEMPLATE_DOWNLOAD
                },
    )
    
    format_to_parquet_task = PythonOperator(
        task_id = "format_to_parquet_task",
        python_callable = format_to_parquet,
        op_kwargs={
            "src_file":PATH_TEMPLATE_DOWNLOAD,
            "final_dir":PATH_TEMPLATE_PARQUET
        }
    )

    local_to_gcs_task = PythonOperator(
    task_id="local_to_gcs_task",
    python_callable=upload_to_gcs,
    op_kwargs={
        "bucket": BUCKET,
        "object_name": PATH_TEMPLATE_GSC,
        "local_file": PATH_TEMPLATE_PARQUET,
    },
)

dowload_data_wse_task >> format_to_parquet_task  >>  local_to_gcs_task  

