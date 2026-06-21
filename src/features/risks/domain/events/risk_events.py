from dataclasses import dataclass
from src.core.events import DomainEvent
from uuid import UUID
from typing import Any


@dataclass
class RiskCreatedEvent(DomainEvent):
    risk_ref: str
    risk_discription: str
    occurence: int
    significance: int
    score: int
    objective_id: UUID
    component_id: UUID

    def to_dict(self) -> dict[Any, Any]:
        return {
            **super().to_dict(),
            "event_type": "risk.created",
            "risk_ref": self.risk_ref,
            "risk_discreption": self.risk_discription,
            "score": self.score,
            "occurence": self.occurence,
            "significance": self.significance,
            "objective_id": str(self.objective_id),
            "component_id": str(self.component_id),
        }
