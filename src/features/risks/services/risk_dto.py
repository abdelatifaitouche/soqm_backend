from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class RiskList:
    id: UUID
    risk_ref: str
    score: int
    occurence: int
    significance: int
    status: str
    risk_description: str


@dataclass(frozen=True)
class PaginatedResponse:
    total: int
    page: int
    size: int
    items: list[RiskList] | None
