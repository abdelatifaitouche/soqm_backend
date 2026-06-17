from dataclasses import dataclass
from uuid import UUID
from datetime import date, datetime
from src.features.risks.enums.risk_states import RiskStatus
from src.core.exceptions import ValidationError
from src.features.soqm_components.domain.component import SOQMComponent
from src.features.quality_objectives.domain.objective import ObjectiveSummary


@dataclass
class Risk:
    id: UUID
    objective_id: UUID
    component_id: UUID
    risk_ref: str
    risk_discription: str
    occurence: int  # 1 - 3
    significance: int  # 1 - 3
    date_identified: date
    status: str = RiskStatus.IDENTIFIED.value
    score: int = 0
    residual_score: float | None = None

    date_last_assessed: date | None = None
    next_review_date: date | None = None

    component: SOQMComponent | None = None
    objective: ObjectiveSummary | None = None

    def calculate_score(self):
        self.score = self.significance * self.occurence
        return self

    def assess(self) -> "Risk":
        if self.status != RiskStatus.IDENTIFIED.value:
            raise ValidationError(
                message="can only assess indentified risk",
            )
        self.status = RiskStatus.ASSESSED.value
        self.date_last_assessed = date.today()
        return self

    def plan_treatment(self) -> "Risk":
        if self.status != RiskStatus.ASSESSED.value:
            raise ValidationError(
                message="must be assessed to plan treatment",
            )
        self.status = RiskStatus.TREATMENT_PLANNED.value
        return self

    def accept(self) -> "Risk":
        self.status = RiskStatus.ACCEPTED.value
        return self

    def close(self) -> "Risk":
        self.status = RiskStatus.CLOSED.value
        return self
