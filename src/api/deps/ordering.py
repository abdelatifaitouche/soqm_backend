from fastapi import Depends

from src.api.schemas.ordering import OrderBy
from src.core.ordering import OrderBy as OrderByEntity


def parse_ordering(order: OrderBy = Depends()) -> OrderByEntity:
    return OrderByEntity(
        columns=order.columns,
        direction=order.direction,
    )
