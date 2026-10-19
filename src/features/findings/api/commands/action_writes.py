from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class UpdateActionRequest(BaseModel):
    title: str | None = None
    finding_id: UUID | None = None
    estimated_completion_date: datetime | None = None


class CreateActionRequest(BaseModel):
    title: str
    finding_id: UUID
    estimated_completion_date: datetime
