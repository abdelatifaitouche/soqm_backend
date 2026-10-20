from uuid import UUID

from pydantic import BaseModel

from src.features.findings.domain.enums.finding import (
    DeficiencySeverity,
    FindingSource,
)


class UpdateFindingRequest(BaseModel):
    finding_title: str | None = None
    finding_source: FindingSource | None = None
    description: str | None = None


class CreateFindingRequest(BaseModel):
    finding_title: str
    description: str
    finding_source: FindingSource
    department: UUID
    deficiency_severity: DeficiencySeverity


class StartRootCauseAnalysisRequest(BaseModel):
    analysis: str
    category_id: UUID
    indicator_id: UUID
    potential_root_cause_id: UUID
    component_id: UUID
