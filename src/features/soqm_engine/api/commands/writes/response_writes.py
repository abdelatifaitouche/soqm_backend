from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field

from src.features.soqm_engine.domain.enums.response_state import (
    ExecutionType,
    Frequency,
    ResponseType,
)


class UpdateResponseRequest(BaseModel):
    response_name: str | None = None
    response_description: str | None = None
    response_type: str | None = None
    frequency: str | None = None
    execution_type: str | None = None


class UpdateResponsesRisksRequest(BaseModel):
    risk_id: UUID


class CreateRiskResponseRequest(BaseModel):
    risks: list[UUID] = Field(min_length=1)
    component_id: UUID
    response_name: str
    response_description: str
    response_type: ResponseType
    response_employee: UUID
    evidence_notes: str
    frequency: Frequency
    execution_type: ExecutionType
    date_implementation: date | None = None
    date_monitored_design: date | None = None
    date_monitored_operating: date | None = None
