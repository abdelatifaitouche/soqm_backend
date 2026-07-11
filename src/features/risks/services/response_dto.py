from dataclasses import dataclass
from uuid import UUID
from datetime import date, datetime


@dataclass(frozen=True)
class ResponseOwner:
    first_name: str
    last_name: str


@dataclass(frozen=True)
class ResponseDetails:
    id: UUID
    response_name: str
    response_ref: str
    status: str
    response_type: str
    frequency: str
    execution_type: str
    owner: ResponseOwner
    evidence_notes: str
    response_description: str
    created_at: datetime
    updated_at: datetime
    # dates
    date_implementation: date | None = None
    date_monitored_design: date | None = None
    date_monitored_operating: date | None = None


@dataclass(frozen=True)
class ResponseList:
    id: UUID
    response_name: str
    response_ref: str
    status: str
    response_type: str
    frequency: str
    execution_type: str
    owner: ResponseOwner


@dataclass(frozen=True)
class PaginatedResponse:
    total: int
    page: int
    size: int
    items: list[ResponseList] | None = None
