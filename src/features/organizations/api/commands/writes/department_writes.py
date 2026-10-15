from pydantic import BaseModel
from uuid import UUID


class CreateDepartmentRequest(BaseModel):
    name: str
    parent_id: UUID | None = None
