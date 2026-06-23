from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class ObjectiveOption(BaseModel):
    id: UUID
    ref: str
    model_config = {"from_attributes": True}


class ObjectiveSummary(BaseModel):
    id: UUID
    objective_reference: str | None = None
    objective_text: str
    status: str
    model_config = {"from_attributes": True}


class CreateObjective(BaseModel):
    objective_text: str
    description: str
    review_date: datetime
    component_id: UUID


class ReadObjective(BaseModel):
    id: UUID
    objective_text: str
    objective_reference: str | None = None
    description: str
    review_date: datetime
    component_id: UUID
    status: str
    updated_at: datetime | None = None
    model_config = {"from_attributes": True}


class UpdateObjective(BaseModel):
    objective_text: str | None = None
    description: str | None = None
    review_date: datetime | None = None
    component_id: UUID | None = None
    status: str | None = None
