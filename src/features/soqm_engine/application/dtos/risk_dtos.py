from dataclasses import dataclass
from uuid import UUID
from datetime import date


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
