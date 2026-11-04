"""Reference Airflow DAG; configure Airflow connections and deploy dependencies separately."""
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="orders_api_to_snowflake_dbt",
    description="Ingest order events and build dbt warehouse models",
    start_date=datetime(2025, 1, 1),
    schedule="@hourly",
    catchup=False,
    default_args=default_args,
    max_active_runs=1,
    tags=["data-engineering", "snowflake", "dbt"],
) as dag:
    ingest = BashOperator(
        task_id="ingest_api_to_landing",
        bash_command="python -m ingestion.run --endpoint orders",
        env={"PYTHONPATH": "/opt/airflow/project/src"},
    )
    transform = BashOperator(
        task_id="dbt_build",
        bash_command="cd /opt/airflow/project/dbt && dbt build",
    )
    ingest >> transform
