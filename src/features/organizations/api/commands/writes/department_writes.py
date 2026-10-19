from uuid import UUID

from pydantic import BaseModel


class CreateDepartmentRequest(BaseModel):
    name: str
    parent_id: UUID | None = None
