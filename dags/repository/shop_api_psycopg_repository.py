from abc import ABC, abstractmethod

from data_models.customer_research_model import CustomerResearchModel
from data_models.user_activity_log_model import UserActivityModel
from data_models.user_order_log_model import UserOrderModel


class ShopAPIRepository(ABC):

    @abstractmethod
    def save_order_logs(self, order_logs: list[UserOrderModel]):
        raise NotImplementedError

    @abstractmethod
    def save_activity_logs(self, activity_logs: list[UserActivityModel]):
        raise NotImplementedError

    @abstractmethod
    def save_customer_research(self, research: list[CustomerResearchModel]):
        raise NotImplementedError
