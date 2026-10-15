from typing import Any

from sqlalchemy import Select


def apply_filters(stmt: Select[Any], conditions: list[Any]) -> Select[Any]:
    for cnd in conditions:
        stmt.where(cnd)
    return stmt
