from pydantic import BaseModel
from uuid import UUID
from enum import StrEnum


class OrderByEnum(StrEnum):
    SCORE = "score"
    CREATED_AT = "created_at"


class OrderDirection(StrEnum):
    ASC = "ASC"
    DESC = "DESC"


class RiskFilters(BaseModel):
    score: int | None = None
    status: str | None = None
    component_id: UUID | None = None


class RiskOrderFilter(BaseModel):
    order_by: OrderByEnum = OrderByEnum.CREATED_AT
    direction: OrderDirection = OrderDirection.DESC
