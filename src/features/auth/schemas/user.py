from pydantic import BaseModel
from uuid import UUID


class UserRead(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    is_active: bool

    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    email: str
    password: str


class CreateUser(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
