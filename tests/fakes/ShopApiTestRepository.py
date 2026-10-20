import uuid

import psycopg
from psycopg import sql
from repository.shop_api_postgres_repository import ShopAPIPostgresRepository


class ShopAPITestPostgresRepository(ShopAPIPostgresRepository):
    def __init__(self):
        self.conn_info = {
            'user': 'airflow',
            'password': 'airflow',
            'dbname': 'airflow',
            'host': 'localhost',
            'port': 5432,
            'autocommit': True,
        }
        self.dbid = None

    def create_test_db(self):
        with psycopg.connect(**self.conn_info) as conn:
            self.dbid = f'aftest_{uuid.uuid4().hex}'
            conn.execute(
                sql.SQL('CREATE DATABASE {}').format(sql.Identifier(self.dbid))
            )
            self.conn_info["dbname"] = self.dbid

    def drop_test_db(self):
        if self.dbid is None:
            return

        self.conn_info['dbname'] = 'airflow'
        with psycopg.connect(**self.conn_info) as conn:
            conn.execute(
                """
                SELECT pg_terminate_backend(pid)
                FROM pg_stat_activity
                WHERE datname = %s AND pid <> pg_backend_pid()
                """,
                [self.dbid],
            )
            conn.execute(
                sql.SQL('DROP DATABASE IF EXISTS {}').format(
                    sql.Identifier(self.dbid)
                )
            )
        self.dbid = None
