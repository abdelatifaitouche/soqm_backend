from dataclasses import dataclass
from uuid import UUID


@dataclass
class UserLogin:
    email: str
    password: str


@dataclass
class UserCreate:
    first_name: str
    last_name: str
    password: str
    email: str
    role_id: UUID


@dataclass
class User:
    id: UUID
    email: str
    is_active: bool
    first_name: str
    last_name: str
    roles: list[str] | None = None
    password_hashed: str | None = None
