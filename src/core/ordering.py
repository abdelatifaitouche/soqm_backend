from sqlalchemy import Select, asc, desc
from typing import Any
from enum import StrEnum
from dataclasses import dataclass


class OrderDirection(StrEnum):
    ASC = "asc"
    DESC = "desc"


@dataclass(frozen=True)
class OrderBy:
    column: str = "created_at"
    direction: OrderDirection = OrderDirection.DESC


class OrderingException(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


def apply_ordering(
    stmt: Select[Any], column: Any, direction: OrderDirection
) -> Select[Any]:
    """
    Dynamicaly order based on the order of type OrderBy object,

    Args:
        stmt : statment to modify
        order : OrderBy object (column, direction : ASC,DESC)

    Returns:
        stmt : a mutated statement to modify having the ordering included
    """
    if direction == OrderDirection.ASC:
        return stmt.order_by(asc(column))
    return stmt.order_by(desc(column))


def resolve_order_column(
    model: Any,
    field: str,
    allowed_fields: dict[str, Any],
) -> Any:
    try:
        return allowed_fields[field]
    except KeyError:
        raise OrderingException(
            f"Ordering by {field} is not allowed for {model.__name__}",
        )
