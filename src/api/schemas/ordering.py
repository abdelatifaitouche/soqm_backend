from pydantic import BaseModel
from src.core.ordering import OrderDirection


class OrderBy(BaseModel):
    column: str = "created_at"
    direction: OrderDirection = OrderDirection.DESC
