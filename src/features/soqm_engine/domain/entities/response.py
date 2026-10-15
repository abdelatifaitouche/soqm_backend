from dataclasses import dataclass, field
from datetime import date, datetime
from uuid import UUID, uuid4

from src.features.soqm_engine.domain.enums.response_state import (
    Frequency,
    ResponseState,
    ResponseType,
)


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
    risks: list[UUID] = field(default_factory=list)

    date_implementation: date | None = None
    date_monitored_design: date | None = None
    date_monitored_operating: date | None = None

    created_at: datetime | None = None
    updated_at: datetime | None = None

    @classmethod
    def create(
        cls,
        *,
        component_id: UUID,
        response_ref: str,
        risks: list[UUID],
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
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        return response

    def update(
        self,
        *,
        response_name: str | None,
        response_description: str | None,
        response_type: str | None,
        frequency,
        execution_type,
    ):
        if response_name and len(response_name) > 10:
            self.response_name = response_name

        if response_description and len(response_description):
            self.response_description = response_description

        if response_type:
            self.response_type = response_type

        if frequency:
            self.frequency = frequency

        if execution_type:
            self.execution_type = execution_type

    def add_risk(self, risk_id: UUID):
        if risk_id not in self.risks:
            self.risks.append(risk_id)

    def remove_risk(self, risk_id: UUID):
        if risk_id not in self.risks:
            raise Exception("Invalid risk id")

        self.risks.remove(risk_id)
