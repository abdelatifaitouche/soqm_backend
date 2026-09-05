from dataclasses import dataclass
from uuid import UUID, uuid4
from src.features.quality_objectives.domain.objective import Objective
from src.features.soqm_components.enums.soqm_component import ComponentState
from src.core.exceptions import ValidationError


@dataclass
class SOQMComponent:
    id: UUID
    name: str
    isqm_reference: str
    status: str
    display_order: int
    description: str | None = None

    @classmethod
    def create(
        cls,
        *,
        name: str,
        isqm_reference: str,
        display_order: int,
        description: str,
    ) -> "SOQMComponent":

        if display_order < 0 or display_order > 8:
            raise ValidationError("Component Order must be between 1 - 8")

        if not name or name.strip() == "":
            raise ValidationError(
                "Component Name must be added",
            )
        if description.strip() == "" or not description:
            raise ValidationError("Component muse have a description")
        component = cls(
            id=uuid4(),
            name=name,
            isqm_reference=isqm_reference,
            display_order=display_order,
            description=description,
            status=ComponentState.ACTIVE.value,
        )
        return component

    def deactivate(self):
        if self.status == ComponentState.IN_ACTIVE.value:
            raise ValidationError("Component Already deactivated")
        self.status = ComponentState.IN_ACTIVE.value

    def activate(self):
        if self.status == ComponentState.ACTIVE.value:
            raise ValidationError("Component Already Activated")

        self.status = ComponentState.ACTIVE

    def archive(self):
        if self.status in (ComponentState.ARCHIVED.value,):
            raise ValidationError(
                "Cannot archive a component in this state",
                details={"state": self.status},
            )

        self.status = ComponentState.ARCHIVED.value

    def _ensure_can_update(self):
        if self.status == ComponentState.ARCHIVED.value:
            raise ValidationError(
                message="Cannot update a component",
                details={"staate": self.status},
            )

    def update_details(
        self,
        name: str | None = None,
        order: int | None = None,
        reference: str | None = None,
        description: str | None = None,
    ):
        self._ensure_can_update()

        if name:
            self.name = name

        if order:
            self.display_order = order

        if reference:
            self.isqm_reference = reference

        if description:
            self.description = description

    def get_status(self) -> str:
        return self.status
