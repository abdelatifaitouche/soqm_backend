from dataclasses import dataclass
from uuid import UUID, uuid4
from datetime import datetime
from src.features.quality_objectives.enums.objective_states import ObjectiveState
from src.core.exceptions import ValidationError


@dataclass
class ObjectiveSummary:
    id: UUID
    status: str
    objective_reference: str | None = None


@dataclass
class Objective:
    id: UUID
    description: str
    review_date: datetime
    component_id: UUID
    status: str
    updated_at: datetime | None = None

    objective_reference: str | None = None

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
            raise ValidationError(
                "Invalid Objective description",
            )

        if not objective_reference or objective_reference.strip() == "":
            raise ValidationError(
                "Invalid Objective reference",
            )

        if review_date <= datetime.now():
            raise ValidationError(
                "Invalid Review date for objective",
            )

        objective = cls(
            id=uuid4(),
            objective_reference=objective_reference,
            review_date=review_date,
            component_id=component_id,
            description=description,
            status=ObjectiveState.DRAFT,
        )

        return objective

    def approve(self):
        """TRANSITION FROM DRAFT TO APPROVED"""
        if self.status != "draft":
            raise ValidationError(
                message=f"Cannot approve objective in {self.status} state",
            )

        self.status = ObjectiveState.APPROVED.value

        return self

    def activate(self):
        """TRANSITION FROM APPROVED TO ACTIVE"""

        if self.status != "approved":
            raise ValidationError(
                message=f"Cannot activate objective in {self.status} state"
            )

        self.status = ObjectiveState.ACTIVE.value

        return self

    def suspend(self):
        if self.status != "active":
            raise ValidationError(
                message="Cannot suspend a non active objective",
            )
        self.status = ObjectiveState.SUSPENDED.value
        return self

    def resume(self):
        if self.status != "suspend":
            raise ValidationError(message="Invalid State for resuming")
        self.status = ObjectiveState.ACTIVE.value
        return self

    def archive(self):
        if self.status != "suspended":
            raise ValidationError(
                message="Cannot archive a non suspended objective",
            )
        self.status = ObjectiveState.SUSPENDED.value
        return self


@dataclass
class UpdateObjective:
    description: str | None = None
    component_id: UUID | None = None
    status: str | None = None
    review_date: datetime | None = None
