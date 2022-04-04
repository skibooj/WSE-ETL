from datetime import datetime
import os

from airflow.operators.bash import BashOperator

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.transfers.gcs_to_gcs import GCSToGCSOperator

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")

TODAY_DATE = "{{ execution_date.strftime('%d-%m-%Y') }}"
SEC_TYPE = "10"
PATH_TO_LOCAL_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
PATH_TEMPLATE_PARQUET = f"{PATH_TO_LOCAL_HOME}/{TODAY_DATE}.parquet"
PATH_TEMPLATE_GSC = f"stock/wse/shares/{{{{ execution_date.strftime('%Y') }}}}/{{{{ execution_date.strftime('%m') }}}}/wse_shares_{TODAY_DATE}.parquet"
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", "wse_data_all")

DATASET = "wse-shares"
INPUT_FILETYPE = "parquet"

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}

# NOTE: DAG declaration - using a Context Manager (an implicit way)
with DAG(
    dag_id="transformation_dag",
    schedule_interval="0 21 * * 1-5",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=["wse"],
) as dag:

    execute_dbt_task = BashOperator(
        task_id="dbt_streamify_run",
        bash_command="cd /dbt && dbt build --profiles-dir . --target prod",
    )
