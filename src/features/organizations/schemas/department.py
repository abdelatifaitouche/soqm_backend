from pydantic import BaseModel
from uuid import UUID


class DeptCompact(BaseModel):
    id: UUID
    name: str
    model_config = {"from_attributes": True}


class Department(BaseModel):
    id: UUID
    name: str
    parent_dept: UUID | None = None
    children_dept: list[DeptCompact] | None = None
    model_config = {"from_attributes": True}


class CreateDepartment(BaseModel):
    name: str
    parent_dept: UUID | None = None
