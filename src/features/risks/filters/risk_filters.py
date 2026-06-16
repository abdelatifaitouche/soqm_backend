from pydantic import BaseModel
from uuid import UUID


class RiskFilters(BaseModel):
    score: int | None = None
    status: str | None = None
    component_id: UUID | None = None
    objective_id: UUID | None = None
