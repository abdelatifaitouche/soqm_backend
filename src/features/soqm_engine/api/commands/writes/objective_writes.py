from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class UpdateObjectiveRequest(BaseModel):
    description: str | None = None
    review_date: datetime | None = None
    component_id: UUID | None = None


class CreateObjectiveRequest(BaseModel):
    description: str
    review_date: datetime
    component_id: UUID
