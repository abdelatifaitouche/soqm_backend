from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass(frozen=True)
class CreateObjective:
    description: str
    review_date: datetime
    component_id: UUID
