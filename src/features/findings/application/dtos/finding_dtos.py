from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.features.findings.domain.entities.finding import RootCauseAnalysis
from src.features.findings.domain.enums.finding import (
    DeficiencySeverity,
    FindingSource,
    FindingStatus,
)


@dataclass(frozen=True)
class UpdateFinding:
    finding_title: str | None = None
    description: str | None = None
    finding_source: FindingSource | None = None


@dataclass(frozen=True)
class CreateFinding:
    finding_title: str
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
    finding_title: str | None = None


@dataclass(frozen=True)
class PaginatedResponse:
    total: int
    page: int
    size: int
    items: list[FindingListItem] | None


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
    finding_title: str | None = None
