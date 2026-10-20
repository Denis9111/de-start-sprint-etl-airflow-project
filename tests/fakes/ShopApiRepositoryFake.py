from repository.shop_api_psycopg_repository import ShopAPIRepository


class ShopAPIRepositoryFake(ShopAPIRepository):
    def __init__(self):
        self.order_logs = []
        self.activity_logs = []
        self.customer_research = []

    def save_order_logs(self, order_logs):
        self.order_logs.extend(order_logs)

    def save_activity_logs(self, activity_logs):
        self.activity_logs.extend(activity_logs)

    def save_customer_research(self, research):
        self.customer_research.extend(research)
