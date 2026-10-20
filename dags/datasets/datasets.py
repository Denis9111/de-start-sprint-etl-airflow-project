from airflow.datasets import Dataset

order_log_dataset = Dataset(
                "postgres://rc1b-ibh8zlbmuynmtr4i.mdb.yandexcloud.net.cdm.f_order")

activity_log_dataset = Dataset(
                "postgres://rc1b-ibh8zlbmuynmtr4i.mdb.yandexcloud.net.cdm.f_activity")

customer_dataset = Dataset(
                "postgres://rc1b-ibh8zlbmuynmtr4i.mdb.yandexcloud.net.cdm.d_customer")

customer_research_dataset = Dataset(
                "postgres://rc1b-ibh8zlbmuynmtr4i.mdb.yandexcloud.net.cdm.f_customer_research")
