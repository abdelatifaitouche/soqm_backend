from pydantic import BaseModel
from uuid import UUID


class UserRead(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    is_active: bool
    roles: list[str] | None = None
    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    email: str
    password: str


class CreateUser(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    role_id: UUID


class AssignRoleRequest(BaseModel):
    role_id: UUID
