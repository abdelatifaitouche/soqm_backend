from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ResponseOwner:
    first_name: str
    last_name: str


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
