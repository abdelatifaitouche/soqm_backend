from src.core.ordering import OrderBy as OrderByEntity
from src.api.schemas.ordering import OrderBy
from fastapi import Depends


def parse_ordering(order: OrderBy = Depends()) -> OrderByEntity:
    return OrderByEntity(
        columns=order.columns,
        direction=order.direction,
    )
