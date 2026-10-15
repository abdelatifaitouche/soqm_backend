from typing import Any

from sqlalchemy import Select

from src.core.pagination import Pagination


def apply_pagination(stmt: Select[Any], pagination: Pagination) -> Select[Any]:
    return stmt.offset(pagination.offset).limit(pagination.limit)


def apply_ordering(
    stmt: Select[Any], model, field: str, direction: str = "asc"
) -> Select[Any]:
    col = getattr(model, field, None)
    if not col:
        return stmt
    return stmt.order_by(col.asc() if direction == "asc" else col.desc())
