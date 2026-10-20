from datetime import timedelta
from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from repository.shop_api_postgres_repository import ShopAPIPostgresRepository

MIGRATION_FOLDER = Path(__file__).resolve().parent / 'migrations'

UPDATE_VERSION_QUERY = """INSERT INTO meta.table_info (version)
                            VALUES (%s)"""

META_SCHEMA_DDL = 'CREATE SCHEMA IF NOT EXISTS meta'

META_TABLE_DDL = """
CREATE TABLE IF NOT EXISTS  meta.table_info
(
    version BIGINT,
    change_date   TIMESTAMP DEFAULT current_timestamp,
    PRIMARY KEY (version)
);
"""
default_args = {
    'owner': 'airflow',
    'concurrency': 1,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}


def run_migration(**kwargs):
    repo = kwargs.get('repo')
    if repo is None:
        repo = ShopAPIPostgresRepository()

    repo.execute_postgres_query(query=META_SCHEMA_DDL, params=[])
    repo.execute_postgres_query(query=META_TABLE_DDL, params=[])
    current_version = repo.get_db_version()

    for file in sorted(MIGRATION_FOLDER.glob('*.sql')):
        version = int(file.stem)
        if current_version is None or version > int(current_version):
            print('Updating database to version: ', version)
            query = get_sql_query_from_file(file)
            print('executing query \n', query)
            repo.execute_postgres_query_batch(queries_list=[query, UPDATE_VERSION_QUERY],
                                              params_list=[[], [version]])
            print('done')


def get_sql_query_from_file(sql_file):
    with open(sql_file, 'r', encoding='utf-8') as f:
        query = f.read()
    return query


with DAG(
        dag_id='db_migrator',
        default_args=default_args,
        start_date=days_ago(2),
        schedule_interval='@once',
        max_active_runs=1,
        catchup=False,
        tags=['Postgres']
) as dag:
    db_task = PythonOperator(
        task_id='db_task',
        python_callable=run_migration,
    )

    db_task
