from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UpdateObjectiveRequest(BaseModel):
    description: str | None = None
    review_date: datetime | None = None
    component_id: UUID | None = None


class CreateObjectiveRequest(BaseModel):
    description: str
    review_date: datetime
    component_id: UUID
