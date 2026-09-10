from uuid import UUID, uuid4
from datetime import datetime
from dataclasses import dataclass
from src.features.soqm_engine.domain.exceptions.objective_exceptions import (
    InvalidObjectiveException,
    InvalidObjectiveStateException,
)
from src.features.soqm_engine.domain.enums.objective_state import ObjectiveState


@dataclass
class Objective:
    id: UUID
    description: str
    review_date: datetime
    component_id: UUID
    status: str
    updated_at: datetime | None = None
    created_at: datetime | None = None
    objective_reference: str | None = None
    lock_version: int | None = None

    @classmethod
    def create(
        cls,
        *,
        description: str,
        review_date: datetime,
        component_id: UUID,
        objective_reference: str,
    ) -> "Objective":

        if not description or description.strip() == "":
            raise InvalidObjectiveException(
                "Invalid Objective description",
            )

        if not objective_reference or objective_reference.strip() == "":
            raise InvalidObjectiveException(
                "Invalid Objective reference",
            )

        if review_date <= datetime.now():
            raise InvalidObjectiveException(
                "Invalid Review date for objective",
            )

        objective = cls(
            id=uuid4(),
            objective_reference=objective_reference,
            review_date=review_date,
            component_id=component_id,
            description=description,
            status=ObjectiveState.DRAFT,
            updated_at=datetime.now(),
            created_at=datetime.now(),
        )

        return objective

    def update(
        self,
        description: str | None,
        review_date: datetime | None,
        component_id: UUID | None,
    ):
        if description:
            self.description = description

        if review_date and review_date > datetime.now():
            self.review_date = review_date

        if component_id:
            self.component_id = component_id

        self.updated_at = datetime.now()

    def approve(self):
        """TRANSITION FROM DRAFT TO APPROVED"""
        if self.status != "draft":
            raise InvalidObjectiveStateException(
                f"Cannot approve objective in {self.status} state",
            )

        self.status = ObjectiveState.APPROVED.value

        return self

    def activate(self):
        if self.status != "approved":
            raise InvalidObjectiveStateException(
                f"Cannot activate objective in {self.status} state"
            )
        self.status = ObjectiveState.ACTIVE.value
        return self

    def suspend(self):
        if self.status != "active":
            raise InvalidObjectiveStateException(
                "Cannot suspend a non active objective",
            )
        self.status = ObjectiveState.SUSPENDED.value
        return self

    def resume(self):
        if self.status != "suspend":
            raise InvalidObjectiveStateException(
                "Invalid State for resuming",
            )
        self.status = ObjectiveState.ACTIVE.value
        return self

    def archive(self):
        if self.status != "suspended":
            raise InvalidObjectiveStateException(
                "Cannot archive a non suspended objective",
            )
        self.status = ObjectiveState.SUSPENDED.value
        return self
