from pydantic import BaseModel


class EmployeeFilters(BaseModel):
    status: str | None = None
    department: str | None = None
    level: str | None = None

    model_config = {
        "from_attributes": True,
    }
