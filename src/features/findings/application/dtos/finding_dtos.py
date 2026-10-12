from dataclasses import dataclass
from uuid import UUID
from src.features.findings.domain.enums.finding import FindingSource, DeficiencySeverity


@dataclass(frozen=True)
class CreateFinding:
    description: str
    finding_source: FindingSource
    department: UUID
    deficiency_severity: DeficiencySeverity
