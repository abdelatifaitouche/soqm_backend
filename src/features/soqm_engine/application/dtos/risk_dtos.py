from dataclasses import dataclass
from uuid import UUID
from datetime import date


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


@dataclass(frozen=True)
class CreateRisk:
    objectives: list[UUID]
    component_id: UUID
    risk_description: str
    occurence: int
    significance: int
    date_identified: date
    status: str
    next_review_date: date


@dataclass(frozen=True)
class ComponentSummary:
    id: UUID
    name: str
    description: str


@dataclass(frozen=True)
class ObjectiveSummary:
    id: UUID
    objective_reference: str
    status: str


@dataclass(frozen=True)
class Risk:
    id: UUID
    risk_ref: str
    risk_description: str
    score: int
    occurence: int
    significance: int
    status: str
    date_last_assessed: date
    next_review_date: date
    residual_score: float
    date_identified: date
    risk_rational: str
    component: ComponentSummary
    objectives: list[ObjectiveSummary]


@dataclass(frozen=True)
class RiskUpdate:
    risk_description: str | None = None
    risk_rational: str | None = None
    occurence: int | None = None
    significance: int | None = None
    next_review_date: date | None = None
