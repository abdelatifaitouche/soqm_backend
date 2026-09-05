from pydantic import BaseModel
from src.core.ordering import OrderDirection


class OrderBy(BaseModel):
    columns: list[str] = [
        "created_at",
    ]
    direction: OrderDirection = OrderDirection.ASC
