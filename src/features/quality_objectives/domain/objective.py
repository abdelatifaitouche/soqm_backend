from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from src.features.quality_objectives.enums.objective_states import ObjectiveState
from src.core.exceptions import ValidationError


@dataclass
class Objective:
    id: UUID
    objective_text: str
    description: str
    review_date: datetime
    component_id: UUID
    status: str = "draft"
    updated_at: datetime | None = None

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
    objective_text: str | None = None
    description: str | None = None
    component_id: UUID | None = None
    status: str | None = None
    review_date: datetime | None = None
