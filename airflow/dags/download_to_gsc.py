import os
import requests
from pathlib import Path
import pandas as pd
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from google.cloud import storage


def gpw_download(date, security_type, path_template) -> None:

    base_url = "https://www.gpw.pl/archiwum-notowan"
    url_params = {"fetch": "1", "type": security_type, "date": date}

    resp = requests.get(base_url, params=url_params, verify=False)
    # Path(path_template).parents[0].mkdir(parents=True, exist_ok=True)

    with Path(path_template).open(mode="wb") as output:
        output.write(resp.content)


def format_to_parquet(src_file, final_dir):
    df = pd.read_excel(src_file)
    df.to_parquet(final_dir)


def upload_to_gcs(bucket, object_name, local_file):
    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)


def delete_file_locally(path_to_delete):
    try:
        for file in path_to_delete:
            os.unlink(file)
    except:
        print("error")


def download_parquetize_upload_dag(
    dag,
    date_to_download,
    security_to_dowload,
    gcp_bucket,
    download_path,
    parquet_path,
    gsc_path,
    files_to_delete,
):

    with dag:
        dowload_data_wse_task = PythonOperator(
            task_id="dowload_data_wse_task",
            python_callable=gpw_download,
            op_kwargs={
                "date": date_to_download,
                "security_type": security_to_dowload,
                "path_template": download_path,
            },
        )

        format_to_parquet_task = PythonOperator(
            task_id="format_to_parquet_task",
            python_callable=format_to_parquet,
            op_kwargs={"src_file": download_path, "final_dir": parquet_path},
        )

        local_to_gcs_task = PythonOperator(
            task_id="local_to_gcs_task",
            python_callable=upload_to_gcs,
            op_kwargs={
                "bucket": gcp_bucket,
                "object_name": gsc_path,
                "local_file": parquet_path,
            },
        )

        delete_files_task = PythonOperator(
            task_id="delete_files_task",
            python_callable=delete_file_locally,
            op_kwargs={"path_to_delete": files_to_delete},
        )

    dowload_data_wse_task >> format_to_parquet_task >> local_to_gcs_task >> delete_files_task


PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")
TODAY_DATE = "{{ execution_date.strftime('%d-%m-%Y') }}"
SEC_TYPE = "10"
PATH_TO_LOCAL_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
PATH_TEMPLATE_DOWNLOAD = f"{PATH_TO_LOCAL_HOME}/{TODAY_DATE}.xls"
PATH_TEMPLATE_PARQUET = f"{PATH_TO_LOCAL_HOME}/{TODAY_DATE}.parquet"
PATH_TEMPLATE_GSC = f"stock/wse/shares/{{{{ execution_date.strftime('%Y') }}}}/{{{{ execution_date.strftime('%m') }}}}/wse_shares_{TODAY_DATE}.parquet"
FILES = [PATH_TEMPLATE_DOWNLOAD, PATH_TEMPLATE_PARQUET]


default_args = {
    "owner": "airflow",
    "start_date": datetime(2019, 1, 1),
    "depends_on_past": False,
    "retries": 1,
}

wse_shares_download_dag = DAG(
    dag_id="wse_shares_download",
    schedule_interval="0 18 * * 1-5",
    default_args=default_args,
    catchup=True,
    max_active_runs=10,
    tags=["wse"],
)


download_parquetize_upload_dag(
    dag=wse_shares_download_dag,
    date_to_download=TODAY_DATE,
    security_to_dowload=SEC_TYPE,
    gcp_bucket=BUCKET,
    download_path=PATH_TEMPLATE_DOWNLOAD,
    parquet_path=PATH_TEMPLATE_PARQUET,
    gsc_path=PATH_TEMPLATE_GSC,
    files_to_delete=FILES,
)
