from dataclasses import dataclass, field
from uuid import UUID
from datetime import date, datetime
from src.features.risks.enums.risk_states import RiskStatus
from src.core.exceptions import ValidationError
from src.features.soqm_components.domain.component import SOQMComponent
from src.features.quality_objectives.domain.objective import ObjectiveSummary
from src.features.risks.domain.events.risk_events import RiskCreatedEvent
from src.core.events import DomainEvent
import uuid


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

    created_by: UUID | None = None

    _events: list[DomainEvent] = field(default_factory=list, init=False, repr=False)

    @classmethod
    def create(
        cls,
        *,
        objective_id,
        component_id,
        risk_ref: str,
        risk_discription: str,
        occurence: int,
        significance: int,
        next_review_date: date,
        created_by: UUID,
    ):
        risk = cls(
            id=uuid.uuid4(),
            objective_id=objective_id,
            component_id=component_id,
            risk_ref=risk_ref,
            risk_discription=risk_discription,
            occurence=occurence,
            significance=significance,
            next_review_date=next_review_date,
            created_by=created_by,
            date_identified=date.today(),
        )

        risk.validate()
        risk.calculate_score()

        risk._emit_event(
            RiskCreatedEvent(
                aggrergate_id=risk.id,
                risk_ref=risk.risk_ref,
                risk_discription=risk.risk_discription,
                objective_id=risk.objective_id,
                component_id=risk.component_id,
                occurence=risk.occurence,
                significance=risk.significance,
                score=risk.score,
            ),
        )

        return risk

    def update(
        self,
        *,
        risk_ref: str | None = None,
        risk_discreption: str | None = None,
        occurence: int | None = None,
        significance: int | None = None,
        next_review_date: date | None = None,
    ):
        if risk_ref is not None:
            self.risk_ref = risk_ref

        if risk_discreption is not None:
            self.risk_discription = risk_discreption

        if occurence is not None:
            self.occurence = occurence

        if significance is not None:
            self.significance = significance

        if next_review_date is not None:
            self.next_review_date

        self.validate()
        self.calculate_score()

    def validate(self) -> None:
        if self.occurence <= 0 or self.occurence > 3:
            raise ValidationError(
                message="Occurence must be between 1 AND 3",
                details={
                    "occurence": self.occurence,
                },
            )
        if self.significance <= 0 or self.significance > 3:
            raise ValidationError(
                message="Significance must be between 1 AND 3",
                details={
                    "significance": self.significance,
                },
            )

        if self.date_identified > date.today():
            raise ValidationError(
                message="cannot identify in the future,",
            )

        if self.next_review_date:
            if self.next_review_date <= date.today():
                raise ValidationError(
                    message="next review date must be in the future",
                    details={
                        "next_review_date": self.next_review_date,
                    },
                )

    def clear_events(self):
        """Clear the event list"""
        self._events.clear()

    def pull_events(self):
        events = self._events
        self._events = []
        return events

    def _emit_event(self, event: DomainEvent):
        """Since we are treating this as a mutable object, we just append a new event into the _event list"""
        self._events.append(event)

    def calculate_score(self):
        self.score = self.significance * self.occurence

    def assess(self) -> None:
        if self.status != RiskStatus.IDENTIFIED.value:
            raise ValidationError(
                message="can only assess indentified risk",
            )
        self.status = RiskStatus.ASSESSED.value
        self.date_last_assessed = date.today()

    def plan_treatment(self) -> None:
        if self.status != RiskStatus.ASSESSED.value:
            raise ValidationError(
                message="must be assessed to plan treatment",
            )
        self.status = RiskStatus.TREATMENT_PLANNED.value

    def close(self) -> None:
        self.status = RiskStatus.CLOSED.value
