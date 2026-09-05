from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date
from src.features.risks.enums.risk_states import RiskStatus
from src.core.exceptions import ValidationError
from src.features.soqm_components.schemas.component import BaseComponent
from src.features.quality_objectives.schemas.objective import ObjectiveSummary


class ListRisk(BaseModel):
    id: UUID
    score: int
    significance: int
    occurence: int
    risk_ref: str
    status: str
    risk_description: str
    model_config = {"from_attributes": True}


class PaginatedResponse(BaseModel):
    total: int
    page: int
    size: int
    items: list[ListRisk] | None
    model_config = {
        "from_attributes": True,
    }


class RiskSummary(BaseModel):
    id: UUID
    risk_ref: str
    score: int
    status: str

    model_config = {"from_attributes": True}


class RiskOption(BaseModel):
    id: UUID
    risk_ref: str
    score: int

    model_config = {
        "from_attributes": True,
    }


class CreateRisk(BaseModel):
    objectives: list[UUID] = Field(min_length=1)
    component_id: UUID
    risk_description: str
    occurence: int = Field(
        ge=1,
        le=3,
        description="Likelihood score from 1 to 3",
    )
    significance: int = Field(ge=1, le=3, description="Impact score from 1 to 3")
    date_identified: date = Field(default_factory=date.today)
    status: str = RiskStatus.IDENTIFIED.value

    next_review_date: date


class Risk(BaseModel):
    id: UUID
    risk_ref: str
    risk_description: str
    occurence: int
    significance: int
    date_identified: date
    status: str
    score: int
    created_by: UUID | None
    component: BaseComponent | None = None
    risk_rational: str | None = None
    model_config = {"from_attributes": True}


class UpdateRisk(BaseModel):
    risk_description: str | None = None
    occurence: int | None = None
    significance: int | None = None
    next_review_date: date | None = None
    component_id: UUID | None = None
    objective_id: UUID | None = None
    risk_rational: str | None = None
