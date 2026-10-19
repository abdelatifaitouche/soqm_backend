from dataclasses import dataclass
from datetime import date
from uuid import UUID


@dataclass
class CreateRisk:
    objectives: list[UUID]
    component_id: UUID
    risk_description: str
    occurence: int
    significance: int
    date_identified: date
    next_review_date: date
