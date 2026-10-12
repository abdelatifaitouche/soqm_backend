from dataclasses import dataclass
from uuid import UUID
from src.features.findings.domain.enums.finding import (
    FindingSource,
    DeficiencySeverity,
    FindingStatus,
)
from datetime import datetime
from src.features.findings.domain.entities.finding import RootCauseAnalysis


@dataclass(frozen=True)
class CreateFinding:
    description: str
    finding_source: FindingSource
    department: UUID
    deficiency_severity: DeficiencySeverity


@dataclass(frozen=True)
class FindingListItem:
    id: UUID
    finding_ref: str
    finding_source: FindingSource
    deficiency_severity: DeficiencySeverity
    status: FindingStatus


@dataclass(frozen=True)
class FindingDetails:
    id: UUID
    finding_ref: str
    description: str
    department: UUID
    finding_source: FindingSource
    deficiency_severity: DeficiencySeverity
    status: FindingStatus
    root_cause_analysis: RootCauseAnalysis
    created_at: datetime
    updated_at: datetime
