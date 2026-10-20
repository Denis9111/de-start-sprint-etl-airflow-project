import json
from datetime import datetime

from data_models.customer_research_model import CustomerResearchModel
from fakes.ShopApiRepositoryFake import ShopAPIRepositoryFake
from utils import api_config


def test_customer_research_parser(mocker):
    source = mocker.patch(
        'utils.api_config.get_customer_research',
        return_value=json.dumps([
            {'date_id': '2024-09-19T00:00:00', 'category_id': 1001,
             'geo_id': 1, 'sales_qty': 8, 'sales_amt': 1944},
            {'date_id': '2024-07-20T00:00:00', 'category_id': 10,
             'geo_id': 2, 'sales_qty': 6, 'sales_amt': 1458},
        ]),
    )
    repo = ShopAPIRepositoryFake()

    api_config.get_insert_customer_research(repo=repo)

    source.assert_called_once_with()
    assert repo.customer_research == [
        CustomerResearchModel(date_id=datetime(2024, 9, 19), category_id=1001,
                              geo_id=1, sales_qty=8, sales_amt=1944),
        CustomerResearchModel(date_id=datetime(2024, 7, 20), category_id=10,
                              geo_id=2, sales_qty=6, sales_amt=1458),
    ]
    assert repo.order_logs == []
    assert repo.activity_logs == []


def test_customer_research_xcom_task_id(mocker):
    ti = mocker.Mock()
    ti.xcom_pull.return_value = '[]'
    assert api_config.get_customer_research(ti=ti) == '[]'
    ti.xcom_pull.assert_called_once_with(task_ids='customer_research_query')
