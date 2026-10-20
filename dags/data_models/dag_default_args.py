from datetime import timedelta

default_args = {
    'owner': 'airflow',
    'concurrency': 4, # теперь airflow будет запускать до 4 тасок параллельно если это указано в очередности запуска тасок в даг
    'retries': 3,
    'retry_delay': timedelta(seconds=10),
    'pool' : 'API_pool',
}
