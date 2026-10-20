from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from src.features.organizations.application.dtos.department_dtos import Department


@dataclass(frozen=True)
class CreateEmployee:
    first_name: str
    last_name: str
    department_id: UUID
    job_title: str
    level: str
    user_id: UUID | None = None


@dataclass(frozen=True)
class UpdateEmployee:
    first_name: str | None = None
    last_name: str | None = None
    job_title: str | None = None


@dataclass(frozen=True)
class EmployeeDetails:
    id: UUID
    first_name: str
    last_name: str
    status: str
    job_title: str
    department: Department
    level: str
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class EmployeeListItem:
    id: UUID
    first_name: str
    last_name: str
    status: str
    level: str
    job_title: str
    department: Department


@dataclass(frozen=True)
class PaginatedEmployeeResponse:
    page: int
    size: int
    total: int

    items: list[EmployeeListItem] | None
