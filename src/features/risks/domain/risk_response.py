from dataclasses import dataclass
from uuid import UUID, uuid4
from datetime import date
from src.features.risks.enums.risk_response import ResponseState


@dataclass
class RiskResponse:
    id: UUID
    risk_id: UUID
    response_description: str
    response_type: str
    status: str
    responsible_employee: UUID
    evidence_notes: str
    created_by: UUID

    date_implementation: date | None = None
    date_monitored_design: date | None = None
    date_monitored_operating: date | None = None

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
            status=ResponseState.DRAFT.value,
            date_monitored_operating=date_monitored_operating,
        )

        return response
