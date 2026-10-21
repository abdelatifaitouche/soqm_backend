from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from src.features.findings.domain.enums import ActionState


@dataclass(frozen=True)
class CreateAction:
    title: str
    finding_id: UUID
    estimated_completion_date: datetime
    owner_id: UUID


@dataclass(frozen=True)
class UpdateAction:
    title: str | None = None
    finding_id: UUID | None = None
    estimated_completion_date: datetime | None = None
    owner_id: UUID | None = None


@dataclass(frozen=True)
class EmployeeItem:
    id: UUID
    first_name: str
    last_name: str


@dataclass(frozen=True)
class ActionDetails:
    id: UUID
    title: str
    finding_id: UUID
    status: ActionState
    estimated_completion_date: datetime
    created_at: datetime
    updated_at: datetime
    owner: EmployeeItem | None = None

    completion_date: datetime | None = None


@dataclass(frozen=True)
class ActionListItem:
    id: UUID
    title: str
    status: ActionState
    estimated_completion_date: datetime
    completion_date: datetime | None = None
    owner: EmployeeItem | None = None


@dataclass(frozen=True)
class PaginatedActionResponse:
    total: int
    page: int
    size: int
    items: list[ActionListItem] | None
