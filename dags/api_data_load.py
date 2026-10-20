import json
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.http.operators.http import HttpOperator
from airflow.providers.http.sensors.http import HttpSensor
from data_models.api_pipeline_config import pipeline_config  # импорт конфига
from data_models.dag_default_args import default_args
from utils.api_config import (get_insert_customer_research, get_insert_user_activity_log,
                              get_insert_user_order_log)


def response_check(response):
    response = json.loads(response.text)
    return response['status'] == 'OK'

with DAG('api_data_load',
         default_args=default_args,
         start_date=datetime(2024, 6, 1),
         end_date=datetime(2024, 12, 1),
         schedule_interval='@daily',
         tags=['API', 'Postgres'],
         catchup=True,
         max_active_runs=1) as dag:
    check_api = HttpSensor(
        task_id='check_api',
        http_conn_id=pipeline_config['api_connection'],  # новый способ передать Connection
        endpoint='healthcheck',
        method='GET',
        headers={'Content-Type': 'application/json'},
        response_check=response_check,
        poke_interval=60 * 3,
        timeout=60 * 24,
        mode='reschedule',
        pool ='API_pool'
    )

    clean_order_log = SQLExecuteQueryOperator(
        task_id='clean_order_log',
        conn_id=pipeline_config['db_connection'],  # новый способ передать Connection
        sql=""" DELETE FROM raw.user_order_log
               WHERE date_time::date='{{ ds }}'::date"""
    )

    order_log_query = HttpOperator(
        task_id='order_log_query',
        http_conn_id=pipeline_config['api_connection'],
        endpoint='user_order_log',
        method='POST',
        data=json.dumps({'limit': '20000000', 'filter': {'date': '{{ ds }}'}}),
        headers={'Content-Type': 'application/json'},
        log_response=True,
        pool ='API_pool'
    )

    order_log = PythonOperator(
        task_id='order_log',
        python_callable=get_insert_user_order_log,
        provide_context=True
    )

    clean_activity_log = SQLExecuteQueryOperator(
        task_id='clean_activity_log',
        conn_id=pipeline_config['db_connection'],
        sql=""" DELETE FROM raw.user_activity_log
                 WHERE date_time::date='{{ ds }}'::date"""
    )

    activity_log_query = HttpOperator(
        task_id='activity_log_query',
        http_conn_id=pipeline_config['api_connection'],
        endpoint='user_activity_log',
        method='POST',
        data=json.dumps({'limit': '20000000', 'filter': {'date': '{{ ds }}'}}),
        headers={'Content-Type': 'application/json'},
        log_response=True,
        pool='API_pool'
    )

    activity_log = PythonOperator(
        task_id='activity_log',
        python_callable=get_insert_user_activity_log,
        provide_context=True
    )

    clean_customer_research = SQLExecuteQueryOperator(
        task_id='delete_from_customer_research',
        conn_id=pipeline_config['db_connection'],
        sql="DELETE FROM raw.customer_research WHERE date_id::date = '{{ ds }}'::date",
    )

    customer_research_query = HttpOperator(
        task_id='customer_research_query',
        http_conn_id=pipeline_config['api_connection'],
        endpoint='customer_research',
        method='POST',
        data=json.dumps({'limit': '20000000', 'filter': {'date': '{{ ds }}'}}),
        headers={'Content-Type': 'application/json'},
        log_response=False,
        pool='API_pool',
    )

    customer_research = PythonOperator(
        task_id='customer_research',
        python_callable=get_insert_customer_research,
    )

    (check_api >> clean_order_log >> order_log_query >> order_log >>
     clean_activity_log >> activity_log_query >> activity_log >>
     clean_customer_research >> customer_research_query >> customer_research)
