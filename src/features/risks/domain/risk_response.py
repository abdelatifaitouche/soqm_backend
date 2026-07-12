from dataclasses import dataclass
from uuid import UUID, uuid4
from datetime import date
from src.features.risks.enums.risk_response import ResponseState, ResponseType


@dataclass
class RiskResponse:
    id: UUID
    response_ref: str
    response_name: str
    response_description: str
    response_type: str
    status: str
    owner: UUID
    evidence_notes: str
    created_by: UUID
    component_id: UUID
    frequency: str
    execution_type: str
    risks: list[UUID] | None = None

    date_implementation: date | None = None
    date_monitored_design: date | None = None
    date_monitored_operating: date | None = None

    @classmethod
    def response_create(
        cls,
        *,
        component_id: UUID,
        response_ref: str,
        risks: list[UUID] | None = None,
        response_name,
        response_description,
        response_type,
        date_implementation,
        date_monitored_design,
        date_monitored_operating,
        owner: UUID,
        frequency: str,
        execution_type: str,
        created_by,
        evidence_notes,
    ) -> "RiskResponse":
        """Factory for creating a risk response"""
        response: RiskResponse = cls(
            component_id=component_id,
            id=uuid4(),
            risks=risks,
            response_ref=response_ref,
            response_name=response_name,
            response_description=response_description,
            response_type=response_type,
            date_implementation=date_implementation,
            date_monitored_design=date_monitored_design,
            created_by=created_by,
            evidence_notes=evidence_notes,
            status=ResponseState.DRAFT.value,
            date_monitored_operating=date_monitored_operating,
            owner=owner,
            execution_type=execution_type,
            frequency=frequency,
        )

        return response
