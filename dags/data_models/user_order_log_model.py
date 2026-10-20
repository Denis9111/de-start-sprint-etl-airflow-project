from datetime import datetime

import pydantic


class UserOrderModel(pydantic.BaseModel):
    id: int
    uniq_id: str
    date_time: datetime
    city_id: int
    city_name: str
    customer_id: int
    first_name: str
    last_name: str
    item_id: int
    item_name: str
    quantity: int
    payment_amount: int
