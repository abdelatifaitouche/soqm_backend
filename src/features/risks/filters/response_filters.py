from pydantic import BaseModel
from uuid import UUID


class ResponseFilters(BaseModel):
    status: str | None = None
    risk_id: UUID | None = None
    assigned_employee: UUID | None = None
    created_by: UUID | None = None
    execution_type: str | None = None
    frequency: str | None = None
    component_id: UUID | None = None
