from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class Department:
    id: UUID
    name: str


@dataclass(frozen=True)
class CreateDepartment:
    name: str
    parent_id: UUID | None = None
