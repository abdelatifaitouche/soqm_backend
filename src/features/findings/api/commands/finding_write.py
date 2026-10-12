from pydantic import BaseModel
from uuid import UUID
from src.features.findings.domain.enums.finding import (
    FindingSource,
    FindingStatus,
    DeficiencySeverity,
)


class CreateFindingRequest(BaseModel):
    description: str
    finding_source: FindingSource
    department: UUID
    deficiency_severity: DeficiencySeverity
