from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from src.features.findings.domain.enums.finding import (
    DeficiencySeverity,
    FindingSource,
    FindingStatus,
    ProcessStatus,
)


@dataclass
class RootCauseAnalysis:
    cause_analysis_status: ProcessStatus = ProcessStatus.NOT_STARTED
    analysis: str | None = None

    # References to the root-cause reference data
    category_id: UUID | None = None
    indicator_id: UUID | None = None
    potential_root_cause_id: UUID | None = None
    soqm_component_id: UUID | None = None

    analysis_completed_at: datetime | None = None


@dataclass
class Finding:
    id: UUID
    finding_ref: str
    description: str
    finding_source: FindingSource
    department: UUID
    deficiency_severity: DeficiencySeverity

    status: FindingStatus

    root_cause_analysis: RootCauseAnalysis
    created_at: datetime | None = None
    updated_at: datetime | None = None
    finding_title: str | None = None

    @classmethod
    def create(
        cls,
        *,
        finding_ref: str,
        description: str,
        finding_source: FindingSource,
        department: UUID,
        deficiency_severity: DeficiencySeverity,
        finding_title: str,
    ) -> "Finding":
        finding = cls(
            id=uuid4(),
            finding_ref=finding_ref,
            description=description,
            finding_source=finding_source,
            department=department,
            deficiency_severity=deficiency_severity,
            status=FindingStatus.OPEN,
            root_cause_analysis=RootCauseAnalysis(),
            finding_title=finding_title,
        )
        return finding

    def update(
        self,
        finding_title: str | None = None,
        description: str | None = None,
        finding_source: FindingSource | None = None,
    ):
        if finding_title and finding_title.strip() != "":
            self.finding_title = finding_title
            self.updated_at = datetime.now()
        if description and description.strip() != "":
            self.description = description
            self.updated_at = datetime.now()

        if finding_source:
            self.finding_source = finding_source
            self.updated_at = datetime.now()

    def start_root_cause_analysis(self, root_cause_analysis: RootCauseAnalysis):

        root_cause_analysis.cause_analysis_status = ProcessStatus.COMPLETED
        root_cause_analysis.analysis_completed_at = datetime.now()
        self.root_cause_analysis = root_cause_analysis
        self.status = FindingStatus.UNDER_ASSESSMENT

    def can_accept_new_actions(self) -> bool:
        return self.status != FindingStatus.CLOSED
