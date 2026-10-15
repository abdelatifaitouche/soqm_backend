from uuid import UUID

from pydantic import BaseModel

from src.features.findings.domain.enums.finding import (
    DeficiencySeverity,
    FindingSource,
)


class CreateFindingRequest(BaseModel):
    description: str
    finding_source: FindingSource
    department: UUID
    deficiency_severity: DeficiencySeverity
