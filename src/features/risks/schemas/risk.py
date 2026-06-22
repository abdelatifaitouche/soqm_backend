from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date
from src.features.risks.enums.risk_states import RiskStatus
from src.core.exceptions import ValidationError
from src.features.soqm_components.schemas.component import BaseComponent
from src.features.quality_objectives.schemas.objective import ObjectiveSummary


class RiskSummary(BaseModel):
    id: UUID
    risk_ref: str
    score: int
    status: str

    model_config = {"from_attributes": True}


class ListRisk(BaseModel):
    id: UUID
    score: int
    significance: int
    occurence: int
    objective_id: UUID
    risk_ref: str
    risk_discription: str
    model_config = {"from_attributes": True}


class CreateRisk(BaseModel):
    objective_id: UUID
    component_id: UUID
    risk_ref: str
    risk_discription: str
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
    risk_discription: str
    occurence: int
    significance: int
    date_identified: date
    status: str
    score: int
    created_by: UUID | None
    objective: ObjectiveSummary | None = None
    component: BaseComponent | None = None
    model_config = {"from_attributes": True}


class UpdateRisk(BaseModel):
    risk_ref: str | None = None
    risk_discription: str | None = None
    occurence: int | None = None
    significance: int | None = None
    next_review_date: date | None = None
    component_id: UUID | None = None
    objective_id: UUID | None = None
