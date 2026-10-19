from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class DeptCompact:
    id: UUID
    name: str


@dataclass
class Department:
    id: UUID
    name: str

    created_at: datetime
    updated_at: datetime

    parent_id: UUID | None = None
    # children_dept: list[DeptCompact] | None = None

    @classmethod
    def create(cls, name: str, parent_dept: UUID | None) -> "Department":

        dept = cls(
            id=uuid4(),
            name="",
            parent_id=parent_dept,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        dept.rename(name)

        return dept

    def rename(self, new_name: str):
        normalized_name = new_name.strip()

        if not normalized_name:
            raise ValueError("Invalid Name")

        self.name = normalized_name
        self.updated_at = datetime.now()

    def change_parent(self, new_parent: UUID):
        self.parent_id = new_parent
        self.updated_at = datetime.now()
