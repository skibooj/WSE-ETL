import os
import logging
from datetime import date, datetime
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from google.cloud import storage
import pyarrow.csv as pv
import pyarrow.parquet as pq

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")
AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")


def wse_data_download(url_template,file_template,date,financial_instument):
    import requests
    base_url = url_template
    url_params = {'fetch':'1',
                'type':financial_instument,
                'date':date}

    if not os.path.exists(file_template):
        os.mkdir(file_template)

    resp = requests.get(base_url, params=url_params, verify=False)

    with file_template.open(mode ='wb') as output:
        output.write(resp.content)    


def format_to_parquet(src_file, dest_file):
    if not src_file.endswith('.csv'):
        logging.error("Can only accept source files in CSV format, for the moment")
        return
    table = pv.read_csv(src_file)
    pq.write_table(table, dest_file)


def upload_to_gcs(bucket, object_name, local_file):
    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)


default_args = {
    "owner": "airflow",
    #start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}


def donwload_parquetize_upload_dag(
    dag,
    url_template,
    local_csv_path_template,
    local_parquet_path_template,
    gcs_path_template,
    financial_instrument,
    date
):
    with dag:
        wse_data_download_task = PythonOperator(
            task_id="wse_data_download_task",
            python_callable=format_to_parquet,
            op_kwargs={
                "src_file": local_csv_path_template,
                "dest_file": local_parquet_path_template,
                "fin_ins": financial_instrument,
                "date": date
                },)

        format_to_parquet_task = PythonOperator(
            task_id="format_to_parquet_task",
            python_callable=format_to_parquet,
            op_kwargs={
                "src_file": local_csv_path_template,
                "dest_file": local_parquet_path_template
            },
        )

        local_to_gcs_task = PythonOperator(
            task_id="local_to_gcs_task",
            python_callable=upload_to_gcs,
            op_kwargs={
                "bucket": BUCKET,
                "object_name": gcs_path_template,
                "local_file": local_parquet_path_template,
            },
        )

        rm_task = BashOperator(
            task_id="rm_task",
            bash_command=f"rm {local_csv_path_template} {local_parquet_path_template}"
        )

        wse_data_download_task >> format_to_parquet_task >> local_to_gcs_task >> rm_task



URL_PREFIX = 'https://www.gpw.pl/archiwum-notowan?fetch=1&type='
SECURITY_TYPE = '10'
TODAY_DATE = '{{ wse_stock_data }}'
WSE_URL_TEMPLATE = URL_PREFIX + SECURITY_TYPE + '&instrument=&date={{ execution_date.strftime(\'%d-%m-%Y\') }}'
WSE_CSV_FILE_TEMPLATE = AIRFLOW_HOME + '/stock_data_{{ V }}.xls'
WSE_PARQUET_FILE_TEMPLATE = AIRFLOW_HOME + '/stock_data_{{ execution_date.strftime(\'%d-%m-%Y\') }}.parquet'
WSE_GCS_PATH_TEMPLATE = "raw/stock_data/{{ execution_date.strftime(\'%Y\') }}/stock_data_{{ execution_date.strftime(\'%d-%m-%Y\') }}.parquet"


wse_stock_data = DAG(
    dag_id="wse_stock_data",
    schedule_interval="0 23 * * *",
    start_date=datetime(2019, 1, 1),
    default_args=default_args,
    catchup=True,
    max_active_runs=3,
    tags=['wse-stock-sharses'],
)

donwload_parquetize_upload_dag(
    dag=wse_stock_data,
    url_template=WSE_URL_TEMPLATE,
    local_csv_path_template=WSE_CSV_FILE_TEMPLATE,
    local_parquet_path_template=WSE_PARQUET_FILE_TEMPLATE,
    gcs_path_template=WSE_GCS_PATH_TEMPLATE,
    financial_instrument=SECURITY_TYPE,
    date=TODAY_DATE

)