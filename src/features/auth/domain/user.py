from dataclasses import dataclass
from uuid import UUID


@dataclass
class UserLogin:
    email: str
    password: str


@dataclass
class User:
    id: UUID
    email: str
    password_hashed: str
    is_active: bool
    first_name: str
    last_name: str
    roles: list[str]
