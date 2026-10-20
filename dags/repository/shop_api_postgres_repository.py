import psycopg
from data_models.customer_research_model import CustomerResearchModel
from airflow.hooks.base import BaseHook
from data_models.api_pipeline_config import pipeline_config
from data_models.user_activity_log_model import UserActivityModel
from data_models.user_order_log_model import UserOrderModel
from repository.shop_api_psycopg_repository import ShopAPIRepository


class ShopAPIPostgresRepository(ShopAPIRepository):
    def __init__(self, af_conn: str | None = pipeline_config['db_connection']):
        self.postgres_hook = BaseHook.get_connection(af_conn)
        self.conn_info = {
            'user': self.postgres_hook.login,
            'password': self.postgres_hook.password,
            'dbname': self.postgres_hook.schema,
            'host': self.postgres_hook.host,
            'port': self.postgres_hook.port,
        }

    def save_order_logs(self, order_logs: list[UserOrderModel]):
        with psycopg.connect(
                **self.conn_info
        ) as conn:
            with conn.cursor() as cur:
                for model in order_logs:
                    cur.execute("""INSERT INTO raw.user_order_log(uniq_id,
                                                                    date_time,
                                                                    city_id,
                                                                    city_name,
                                                                    customer_id,
                                                                    first_name,
                                                                    last_name,
                                                                    item_id,
                                                                    item_name,
                                                                    quantity,
                                                                    payment_amount)
                                            VALUES (%(uniq_id)s,
                                                    %(date_time)s,
                                                    %(city_id)s,
                                                    %(city_name)s,
                                                    %(customer_id)s,
                                                    %(first_name)s,
                                                    %(last_name)s,
                                                    %(item_id)s,
                                                    %(item_name)s,
                                                    %(quantity)s,
                                                    %(payment_amount)s);
                                            """, model.model_dump())

    def save_activity_logs(self, activity_logs: list[UserActivityModel]):
        with psycopg.connect(
                **self.conn_info
        ) as conn:
            with conn.cursor() as cur:
                for model in activity_logs:
                    cur.execute("""INSERT INTO raw.user_activity_log(uniq_id,
                                                                       date_time,
                                                                       action_id,
                                                                       customer_id,
                                                                       quantity)
                                            VALUES (%(uniq_id)s,
                                                    %(date_time)s,
                                                    %(action_id)s,
                                                    %(customer_id)s,
                                                    %(quantity)s)
                                                    """, model.model_dump())

    def save_customer_research(self, research: list[CustomerResearchModel]):
        with psycopg.connect(**self.conn_info) as conn:
            with conn.cursor() as cur:
                for model in research:
                    cur.execute(
                        """INSERT INTO raw.customer_research
                           (date_id, category_id, geo_id, sales_qty, sales_amt)
                           VALUES (%(date_id)s, %(category_id)s, %(geo_id)s,
                                   %(sales_qty)s, %(sales_amt)s)""",
                        model.model_dump(),
                    )

    def execute_postgres_query(self, **kwargs):
        query = kwargs['query']
        params = kwargs['params']
        with psycopg.connect(
                **self.conn_info
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)

    def execute_postgres_query_with_result(self, **kwargs):
        query = kwargs['query']
        params = kwargs.get('params')
        with psycopg.connect(
                **self.conn_info
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                data = cur.fetchall()
        return data

    def execute_postgres_query_batch(self, **kwargs):
        queries_list = kwargs['queries_list']
        params_list = kwargs.get('params_list') or [None] * len(queries_list)
        with psycopg.connect(
                **self.conn_info
        ) as conn:
            with conn.cursor() as cur:
                for query, params in zip(queries_list, params_list):
                    cur.execute(query, params)

    def get_db_version(self):
        data = self.execute_postgres_query_with_result(query='SELECT max(version) FROM meta.table_info')
        return data[0][0]
