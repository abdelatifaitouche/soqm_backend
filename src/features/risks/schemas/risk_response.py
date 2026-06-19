from pydantic import BaseModel
from uuid import UUID
from datetime import date
from src.features.risks.enums.risk_response import ResponseType


class RiskResponse(BaseModel):
    id: UUID
    risk_id: UUID
    response_description: str
    response_type: str
    date_implementation: date | None = None
    date_monitored_design: date | None = None
    date_monitored_operating: date | None = None
    status: str
    responsible_employee: UUID
    evidence_notes: str
    created_by: UUID

    model_config = {"from_attributes": True}


class CreateRiskResponse(BaseModel):
    response_description: str
    response_type: ResponseType
    response_employee: UUID
    evidence_notes: str

    date_implementation: date | None = None
    date_monitored_design: date | None = None
    date_monitored_operating: date | None = None
