from pydantic import BaseModel


class UserLogin(BaseModel):
    email: str
    password: str


class CreateUser(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
