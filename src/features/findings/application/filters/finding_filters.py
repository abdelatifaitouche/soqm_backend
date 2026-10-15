from pydantic import BaseModel


class FindingFilters(BaseModel):
    status: str | None = None
    finding_source: str | None = None
    deficiency_severity: str | None = None
