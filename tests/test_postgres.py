from pathlib import Path

import pytest

TESTS_FOLDER = Path(__file__).resolve().parent
PROJECT_FOLDER = TESTS_FOLDER.parent


def read_sql_query(path):
    return path.read_text(encoding='utf-8')


def prepare_data(repo, scripts=()):
    for script in scripts:
        query = read_sql_query(TESTS_FOLDER / 'test_data' / script)
        repo.execute_postgres_query(query=query, params=[])


@pytest.fixture(scope='class')
def prepared_data(test_repo):
    prepare_data(test_repo, ('order_log.sql', 'activity_log.sql'))


@pytest.mark.usefixtures('prepared_data')
class TestRawToOds:
    def test_order_log_is_loaded_without_duplicates(self, test_repo, test_date):
        query = read_sql_query(
            PROJECT_FOLDER / 'dags' / 'sql' / 'insert_ods_user_order_log.sql'
        ).replace('{{ ds }}', test_date)

        test_repo.execute_postgres_query(query=query, params=[])

        rows = test_repo.execute_postgres_query_with_result(
            query="""
                SELECT id, uniq_id
                FROM ods.user_order_log
                ORDER BY id
            """
        )
        assert rows == [
            (9, '9c21f7c5f77249ae60a7c6863f235f00'),
            (10, '4ed55d5f4d8d0a65fcbb5a6209b0f3c5'),
        ]

    def test_activity_log_is_loaded_without_duplicates(
            self, test_repo, test_date
    ):
        query = read_sql_query(
            PROJECT_FOLDER / 'dags' / 'sql' / 'insert_ods_user_activity_log.sql'
        ).replace('{{ ds }}', test_date)

        test_repo.execute_postgres_query(query=query, params=[])

        rows = test_repo.execute_postgres_query_with_result(
            query="""
                SELECT id, uniq_id
                FROM ods.user_activity_log
                ORDER BY id
            """
        )
        assert rows == [
            (2, 'a8cf0aebcf9618129803ff2e14f2e3ff'),
            (3, '3fad646208167a268255b5b16e30b9ba'),
        ]
