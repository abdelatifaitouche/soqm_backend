from uuid import UUID
from pydantic import BaseModel, Field


class CreateEmployee(BaseModel):
    first_name: str = Field(min_length=5)
    last_name: str = Field(min_length=5)
    department_id: UUID
    user_id: UUID | None = None
    job_title: str
    level: str


class EmployeeList(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    department: str
    job_title: str
    status: str
    level: str
    model_config = {"from_attributes": True}


class Employee(BaseModel):
    first_name: str
    last_name: str
    department_id: UUID
    job_title: str
    level: str
    status: str
    user_id: UUID | None = None
    model_config = {"from_attributes": True}


class EmployeeOption(BaseModel):
    id: UUID
    first_name: str
    last_name: str

    model_config = {"from_attributes": True}


class EmployeeProfile(BaseModel):
    id: UUID
    email: str
    first_name: str
    last_name: str
    level: str
    job_title: str
    department: str

    model_config = {
        "from_attributes": True,
    }
