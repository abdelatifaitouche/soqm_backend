from sqlalchemy import Select
from typing import Any


def apply_filters(stmt: Select[Any], conditions: list[Any]) -> Select[Any]:
    for cnd in conditions:
        stmt.where(cnd)
    return stmt
