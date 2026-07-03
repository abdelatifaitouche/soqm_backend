from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class ObjectiveOption(BaseModel):
    id: UUID
    objective_reference: str
    model_config = {"from_attributes": True}


class ObjectiveSummary(BaseModel):
    id: UUID
    objective_reference: str | None = None
    status: str
    model_config = {"from_attributes": True}


class CreateObjective(BaseModel):
    description: str
    review_date: datetime
    component_id: UUID


class ReadObjective(BaseModel):
    id: UUID
    objective_reference: str | None = None
    description: str
    review_date: datetime
    component_id: UUID
    status: str
    updated_at: datetime | None = None
    model_config = {"from_attributes": True}


class UpdateObjective(BaseModel):
    description: str | None = None
    review_date: datetime | None = None
    component_id: UUID | None = None
    status: str | None = None
