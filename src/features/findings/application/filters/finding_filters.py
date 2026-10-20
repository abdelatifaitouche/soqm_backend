from pydantic import BaseModel
from uuid import UUID


class FindingFilters(BaseModel):
    status: str | None = None
    finding_source: str | None = None
    department_id: UUID | None = None
    deficiency_severity: str | None = None
