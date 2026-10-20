from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime


class EmployeeCreatedResponse(BaseModel):
    id: UUID


class Department(BaseModel):
    id: UUID
    name: str
    model_config = {"from_attributes": True}


class EmployeeReadResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    status: str
    job_title: str
    department: Department
    level: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
