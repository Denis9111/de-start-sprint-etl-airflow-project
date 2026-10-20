from pathlib import Path

import pytest
from jinja2 import Template

PROJECT_FOLDER = Path(__file__).resolve().parents[1]


def execute_sql(repo, name, ds='2024-09-01'):
    query = (PROJECT_FOLDER / 'dags' / 'sql' / name).read_text(encoding='utf-8')
    repo.execute_postgres_query(query=Template(query).render(ds=ds), params=[])


class TestMarketShare:
    def test_report_updates_existing_row_and_is_repeatable(self, test_repo):
        data = (PROJECT_FOLDER / 'tests/test_data/market_share.sql').read_text(
            encoding='utf-8'
        )
        test_repo.execute_postgres_query(query=data, params=[])

        for _ in range(2):
            execute_sql(test_repo, 'insert_market_share.sql')
            rows = test_repo.execute_postgres_query_with_result(
                query='SELECT date_time::date::text, city_id, qty_share, amt_share '
                      'FROM rep.market_share_report'
            )
            assert len(rows) == 1
            assert rows[0][:2] == ('2024-09-01', 1)
            assert rows[0][2] == pytest.approx(0.45)
            assert rows[0][3] == pytest.approx(0.6)

        check = (PROJECT_FOLDER / 'dags/sql/check_market_share.sql').read_text(
            encoding='utf-8'
        )
        assert test_repo.execute_postgres_query_with_result(query=check) == []

        # The same dataset also exercises the undefined 0 / 0 case.
        test_repo.execute_postgres_query(
            query='UPDATE cdm.f_order SET quantity=0, payment_amount=0; '
                  'UPDATE cdm.f_customer_research SET sales_qty=0, sales_amt=0',
            params=[],
        )
        execute_sql(test_repo, 'insert_market_share.sql')
        assert test_repo.execute_postgres_query_with_result(
            query='SELECT qty_share, amt_share FROM rep.market_share_report'
        ) == [(None, None)]


class TestCustomerResearchPipeline:
    def test_deduplication_date_filter_and_surrogate_city(self, test_repo):
        test_repo.execute_postgres_query(query="""
            INSERT INTO cdm.d_city (id, city_id, city_name, start_date, end_date)
            OVERRIDING SYSTEM VALUE VALUES
            (1, 77, 'Москва', '2024-01-01', '2024-08-31'),
            (2, 77, 'Москва', '2024-09-01', '9999-12-31');
            INSERT INTO raw.customer_research VALUES
            ('2024-09-01', 1001, 77, 8, 1000),
            ('2024-09-01', 1001, 77, 11, 5000),
            ('2024-09-02', 1001, 77, 999, 999);
        """, params=[])

        for _ in range(2):
            execute_sql(test_repo, 'insert_ods_customer_research.sql')
            execute_sql(test_repo, 'insert_f_customer_research.sql')

        assert test_repo.execute_postgres_query_with_result(
            query='SELECT geo_id, sales_qty, sales_amt FROM ods.customer_research'
        ) == [(77, 11, 5000)]
        assert test_repo.execute_postgres_query_with_result(
            query='SELECT city_id, sales_qty, sales_amt FROM cdm.f_customer_research'
        ) == [(2, 11, 5000)]
