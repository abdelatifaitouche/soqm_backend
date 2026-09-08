from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class CreateObjectiveRequest(BaseModel):
    description: str
    review_date: datetime
    component_id: UUID
