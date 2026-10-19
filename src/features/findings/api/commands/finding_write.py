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


class StartRootCauseAnalysisRequest(BaseModel):
    analysis: str
    category_id: UUID
    indicator_id: UUID
    potential_root_cause_id: UUID
    component_id: UUID
