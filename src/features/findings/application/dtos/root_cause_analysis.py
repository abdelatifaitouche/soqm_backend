from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CreateRootCauseAnalysis:
    analysis: str

    # References to the root-cause reference data
    category_id: UUID
    indicator_id: UUID
    potential_root_cause_id: UUID
