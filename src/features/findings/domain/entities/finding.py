from datetime import datetime
from dataclasses import dataclass
from uuid import UUID, uuid4
from src.features.findings.domain.enums.finding import (
    FindingStatus,
    FindingSource,
    DeficiencySeverity,
)


@dataclass
class Finding:
    id: UUID
    finding_ref: str
    description: str
    finding_source: FindingSource
    department: UUID
    deficiency_severity: DeficiencySeverity

    status: FindingStatus
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @classmethod
    def create(
        cls,
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
        )
        return finding
