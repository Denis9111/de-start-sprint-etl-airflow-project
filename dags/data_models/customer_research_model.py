from datetime import datetime

from pydantic import BaseModel


class CustomerResearchModel(BaseModel):
    date_id: datetime
    category_id: int
    geo_id: int
    sales_qty: int
    sales_amt: int
