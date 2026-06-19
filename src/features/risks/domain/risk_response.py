from dataclasses import dataclass
from uuid import UUID, uuid4
from datetime import date


@dataclass
class RiskResponse:
    id: UUID
    risk_id: UUID
    response_description: str
    response_type: str
    date_implementation: str
    date_monitored_design: date
    date_monitored_operating: date
    status: str
    responsible_employee: UUID
    evidence_notes: str
    created_by: UUID

    @classmethod
    def response_create(
        cls,
        *,
        risk_id,
        response_description,
        response_type,
        date_implementation,
        date_monitored_design,
        date_monitored_operating,
        responsible_employee,
        created_by,
        evidence_notes,
    ) -> "RiskResponse":
        """Factory for creating a risk response"""
        response: RiskResponse = cls(
            id=uuid4(),
            risk_id=risk_id,
            response_description=response_description,
            response_type=response_type,
            date_implementation=date_implementation,
            date_monitored_design=date_monitored_design,
            responsible_employee=responsible_employee,
            created_by=created_by,
            evidence_notes=evidence_notes,
            status="",
            date_monitored_operating=date_monitored_operating,
        )

        return response
