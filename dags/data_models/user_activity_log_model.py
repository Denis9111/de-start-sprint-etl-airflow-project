from datetime import datetime

import pydantic

class UserActivityModel(pydantic.BaseModel):
    id: int
    uniq_id: str
    date_time: datetime
    action_id: int
    customer_id: int
    quantity: int
