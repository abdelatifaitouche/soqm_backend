from uuid import UUID

from pydantic import BaseModel


class UpdateDepartmentRequest(BaseModel):
    name: str


class UpdateDepartmentParentRequest(BaseModel):
    parent_id: UUID


class CreateDepartmentRequest(BaseModel):
    name: str
    parent_id: UUID | None = None
