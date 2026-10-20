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

    @classmethod
    def create(
        cls,
        *,
        finding_ref: str,
        description: str,
        finding_source: FindingSource,
        department: UUID,
        deficiency_severity: DeficiencySeverity,
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
        )
        return finding

    def update(
        self,
        description: str | None,
        finding_source: FindingSource | None,
    ):
        return

    def start_root_cause_analysis(self, root_cause_analysis: RootCauseAnalysis):

        if self.status != FindingStatus.OPEN:
            raise ValueError(
                f"Invalid finding state : {self.status} , state must be OPEN",
            )

        root_cause_analysis.cause_analysis_status = ProcessStatus.COMPLETED
        root_cause_analysis.analysis_completed_at = datetime.now()
        self.root_cause_analysis = root_cause_analysis
        self.status = FindingStatus.UNDER_ASSESSMENT

    def can_accept_new_actions(self) -> bool:
        return self.status != FindingStatus.CLOSED
