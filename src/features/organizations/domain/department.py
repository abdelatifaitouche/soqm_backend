from dataclasses import dataclass
from uuid import UUID


@dataclass
class DeptCompact:
    id: UUID
    name: str


@dataclass
class Department:
    name: str
    parent_dept: UUID | None = None
    children_dept: list[DeptCompact] | None = None
    id: UUID | None = None
