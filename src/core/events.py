from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass(kw_only=True)
class DomainEvent:
    aggrergate_id: UUID
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict[str, str]:
        return {
            "aggregate_id": str(self.aggrergate_id),
            "timestamp": self.timestamp.isoformat(),
        }
