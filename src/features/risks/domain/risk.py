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
class RiskSummary:
    id: UUID
    risk_ref: str
    score: int
    status: str


@dataclass
class Risk:
    id: UUID
    component_id: UUID
    risk_ref: str
    risk_description: str
    occurence: int  # 1 - 3
    significance: int  # 1 - 3
    date_identified: date
    created_at: datetime
    updated_at: datetime
    status: str = RiskStatus.IDENTIFIED.value
    score: int = 0
    residual_score: float | None = None
    sequence: int | None = None

    risk_rational: str | None = None

    objectives: list[UUID] | None = None

    date_last_assessed: date | None = None
    next_review_date: date | None = None

    component: SOQMComponent | None = None

    created_by: UUID | None = None
    _events: list[DomainEvent] = field(default_factory=list, init=False, repr=False)

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
            id=uuid.uuid4(),
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
        )

        risk.validate()
        risk.calculate_score()

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

        self.validate()
        self.calculate_score()
        self.updated_at = datetime.now()

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
