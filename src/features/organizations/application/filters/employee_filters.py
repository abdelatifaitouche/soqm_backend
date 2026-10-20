from pydantic import BaseModel
from uuid import UUID


class EmployeeFilters(BaseModel):
    status: str | None = None
    job_title: str | None = None
    level: str | None = None
    department_id: UUID | None = None
