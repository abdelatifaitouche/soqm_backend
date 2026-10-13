from dataclasses import dataclass
from datetime import datetime, date
from uuid import UUID, uuid4
from src.features.soqm_engine.domain.enums.risk_state import RiskStatus


@dataclass
class Risk:
    id: UUID
    component_id: UUID
    risk_ref: str
    risk_description: str
    occurence: int  # 1 - 3
    significance: int  # 1 - 3
    score: int

    # dates
    date_identified: date
    created_at: datetime
    updated_at: datetime

    residual_score: float | None = None
    sequence: int | None = None

    status: str = RiskStatus.IDENTIFIED.value
    risk_rational: str | None = None

    objectives: list[UUID] | None = None

    date_last_assessed: date | None = None
    next_review_date: date | None = None
    created_by: UUID | None = None

    @classmethod
    def create(
        cls,
        *,
        component_id,
        sequence: int,
        risk_description: str,
        occurence: int,
        significance: int,
        next_review_date: date,
        created_by: UUID,
        objectives: list[UUID],
        component_idx: int,
    ):
        risk = cls(
            id=uuid4(),
            component_id=component_id,
            risk_ref=cls.generate_risk_reference(sequence, component_idx),
            risk_description=risk_description,
            occurence=occurence,
            significance=significance,
            next_review_date=next_review_date,
            created_by=created_by,
            objectives=objectives,
            date_identified=date.today(),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            score=significance * occurence,
        )
        return risk

    @classmethod
    def generate_risk_reference(cls, sequence: int, component_idx: int) -> str:
        return f"{component_idx}.{sequence}"

    def update(
        self,
        *,
        risk_description: str | None = None,
        occurence: int | None = None,
        significance: int | None = None,
        next_review_date: date | None = None,
        risk_rational: str | None = None,
    ):

        if risk_description is not None:
            self.risk_description = risk_description

        if occurence is not None:
            self.occurence = occurence

        if significance is not None:
            self.significance = significance

        if next_review_date is not None:
            self.next_review_date

        if risk_rational:
            self.risk_rational = risk_rational

        self.updated_at = datetime.now()
