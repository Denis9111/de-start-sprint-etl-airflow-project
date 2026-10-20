import json

from data_models.customer_research_model import CustomerResearchModel
from data_models.user_activity_log_model import UserActivityModel
from data_models.user_order_log_model import UserOrderModel
from repository.shop_api_postgres_repository import ShopAPIPostgresRepository


def get_order_log(**kwargs):
    task_instance = kwargs['ti']
    data = task_instance.xcom_pull(task_ids='order_log_query')
    return data


def get_activity_log(**kwargs):
    task_instance = kwargs['ti']
    data = task_instance.xcom_pull(task_ids='activity_log_query')
    return data


def get_insert_user_order_log(repo=None, **kwargs):
    if repo is None:
        repo = ShopAPIPostgresRepository()
    raw_data = get_order_log(**kwargs)
    data = json.loads(raw_data)
    order_logs = [UserOrderModel(**row) for row in data]
    repo.save_order_logs(order_logs)


def get_insert_user_activity_log(repo=None, **kwargs):
    if repo is None:
        repo = ShopAPIPostgresRepository()
    raw_data = get_activity_log(**kwargs)
    data = json.loads(raw_data)
    activity_logs = [UserActivityModel(**row) for row in data]
    repo.save_activity_logs(activity_logs)


def get_customer_research(**kwargs):
    return kwargs['ti'].xcom_pull(task_ids='customer_research_query')


def get_insert_customer_research(repo=None, **kwargs):
    if repo is None:
        repo = ShopAPIPostgresRepository()
    data = json.loads(get_customer_research(**kwargs))
    repo.save_customer_research([CustomerResearchModel(**row) for row in data])
