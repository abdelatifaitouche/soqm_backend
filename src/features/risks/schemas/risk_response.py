from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date
from src.features.risks.enums.risk_response import ResponseType
from src.features.risks.schemas.risk import RiskSummary


class Owner(BaseModel):
    first_name: str
    last_name: str
    model_config = {
        "from_attributes": True,
    }


class Response(BaseModel):
    id: UUID
    response_name: str | None = None
    response_ref: str
    response_type: str
    status: str
    frequency: str
    execution_type: str
    owner: Owner
    date_implementation: date | None = None

    model_config = {"from_attributes": True}


class PaginatedResponse(BaseModel):
    total: int
    size: int
    page: int
    items: list[Response] | None = None

    model_config = {
        "from_attributes": True,
    }


class RiskResponse(BaseModel):
    id: UUID
    response_name: str | None = None
    response_ref: str
    response_description: str
    response_type: str
    date_implementation: date | None = None
    date_monitored_design: date | None = None
    date_monitored_operating: date | None = None
    status: str
    owner: UUID
    evidence_notes: str
    created_by: UUID

    model_config = {"from_attributes": True}


class CreateRiskResponse(BaseModel):
    risks: list[UUID] = Field(min_length=1)
    component_id: UUID
    response_name: str
    response_description: str
    response_type: ResponseType
    response_employee: UUID
    evidence_notes: str

    date_implementation: date | None = None
    date_monitored_design: date | None = None
    date_monitored_operating: date | None = None
