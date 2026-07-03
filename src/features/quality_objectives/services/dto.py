from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass(frozen=True)
class BaseObjective:
    id: UUID
    objective_reference: str


@dataclass(frozen=True)
class ObjectiveList(BaseObjective):
    review_date: datetime
    status: str


@dataclass(frozen=True)
class ObjectiveDetails(BaseObjective):
    review_date: datetime
    status: str
    component_id: UUID
    updated_at: datetime
    created_at: datetime
    description: str
