from pydantic import BaseModel
from uuid import UUID


class CreateEmployeeRequest(BaseModel):
    first_name: str
    last_name: str
    department_id: UUID
    job_title: str
    level: str
    user_id: UUID | None = None


class UpdateEmployeeRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    job_title: str | None = None
