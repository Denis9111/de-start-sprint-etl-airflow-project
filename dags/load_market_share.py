from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from data_models.api_pipeline_config import pipeline_config
from data_models.dag_default_args import default_args
from datasets.datasets import customer_research_dataset, order_log_dataset


with DAG(
    'load_market_share',
    default_args=default_args,
    start_date=datetime(2024, 6, 1),
    schedule=[order_log_dataset, customer_research_dataset],
    catchup=False,
    max_active_runs=1,
    tags=['Postgres', 'market_share'],
) as dag:
    start_task = EmptyOperator(task_id='start_task')
    market_share_report = SQLExecuteQueryOperator(
        task_id='load_market_share_report',
        conn_id=pipeline_config['db_connection'],
        sql='sql/insert_market_share.sql',
    )
    end_task = EmptyOperator(task_id='end_task')

    start_task >> market_share_report >> end_task
