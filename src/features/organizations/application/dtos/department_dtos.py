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


@dataclass(frozen=True)
class UpdateDepartment:
    name: str


@dataclass(frozen=True)
class UpdateDepartmentParent:
    parent_id: UUID
