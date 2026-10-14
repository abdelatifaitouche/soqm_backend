from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date
from src.features.soqm_engine.domain.enums.risk_state import RiskStatus


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


class UpdateRiskRequest(BaseModel):
    risk_description: str | None = None
    risk_rational: str | None = None
    next_review_date: date | None = None


class UpdateRiskObjectiveRequest(BaseModel):
    objective_id: UUID


class UpdateRiskResponseRequest(BaseModel):
    response_id: UUID
