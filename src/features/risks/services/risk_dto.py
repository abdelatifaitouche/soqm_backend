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


@dataclass
class RiskMatrixCell:
    occurence: int
    significance: int
    percent: float


@dataclass
class RiskMatrix:
    cells: list[RiskMatrixCell] | None = None


@dataclass(frozen=True)
class RiskOption:
    id: UUID
    risk_ref: str
    score: int


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
    risk_discreption: str
    score: int
    occurence: int
    significance: int
    status: str
    date_last_assessed: date
    next_review_date: date
    residual_score: float
    date_identified: date
    component: ComponentSummary
    objectives: list[ObjectiveSummary]
