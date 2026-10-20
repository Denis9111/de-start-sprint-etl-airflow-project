import json

from data_models.user_activity_log_model import UserActivityModel
from data_models.user_order_log_model import UserOrderModel
from repository.shop_api_psycopg_repository import ShopAPIRepository
from utils import api_config


def test_get_insert_user_order_log(mocker):
    order_log_json = json.dumps(
        [
            {
                "id": 1,
                "uniq_id": "6086052ae29453fa02991041fdcb4ec3",
                "date_time": "2024-08-29T00:00:00",
                "city_id": 2,
                "city_name": "Ярославль",
                "customer_id": 2518,
                "first_name": "Ольга",
                "last_name": "Лебедева",
                "item_id": 0,
                "item_name": "Молоко 1%",
                "quantity": 2,
                "payment_amount": 200,
            },
            {
                "id": 2,
                "uniq_id": "cb23b5aad3836cf767eb8de21252d7dd",
                "date_time": "2024-08-29T00:00:00",
                "city_id": 1,
                "city_name": "Ростов",
                "customer_id": 4214,
                "first_name": "Екатерина",
                "last_name": "Морозова",
                "item_id": 1,
                "item_name": "Молоко 3%",
                "quantity": 3,
                "payment_amount": 360,
            },
        ],
        ensure_ascii=False,
    )
    get_order_log_mock = mocker.patch(
        "utils.api_config.get_order_log",
        return_value=order_log_json,
    )
    repository_mock = mocker.Mock(spec=ShopAPIRepository)

    api_config.get_insert_user_order_log(repo=repository_mock)

    get_order_log_mock.assert_called_once_with()
    repository_mock.save_order_logs.assert_called_once()
    repository_mock.save_activity_logs.assert_not_called()

    saved_order_logs = repository_mock.save_order_logs.call_args.args[0]
    expected_order_logs = [
        UserOrderModel(**row) for row in json.loads(order_log_json)
    ]
    assert saved_order_logs == expected_order_logs


def test_get_insert_user_activity_log(mocker):
    activity_log_json = json.dumps(
        [
            {
                "id": 1,
                "uniq_id": "d2c991db29f4440fa98fb72c8a1f0011",
                "date_time": "2024-08-29T00:00:00",
                "action_id": 1,
                "customer_id": 2518,
                "quantity": 1,
            },
            {
                "id": 2,
                "uniq_id": "ab941152d25e4731b47112b0c1f0022",
                "date_time": "2024-08-29T01:00:00",
                "action_id": 2,
                "customer_id": 4214,
                "quantity": 3,
            },
        ],
        ensure_ascii=False,
    )
    get_activity_log_mock = mocker.patch(
        "utils.api_config.get_activity_log",
        return_value=activity_log_json,
    )
    repository_mock = mocker.Mock(spec=ShopAPIRepository)

    api_config.get_insert_user_activity_log(repo=repository_mock)

    get_activity_log_mock.assert_called_once_with()
    repository_mock.save_activity_logs.assert_called_once()
    repository_mock.save_order_logs.assert_not_called()

    saved_activity_logs = repository_mock.save_activity_logs.call_args.args[0]
    expected_activity_logs = [
        UserActivityModel(**row) for row in json.loads(activity_log_json)
    ]
    assert saved_activity_logs == expected_activity_logs
