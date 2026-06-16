from src.features.risks.domain.risk import Risk
from src.features.quality_objectives.repository.objective_repository import (
    ObjectiveRepository,
)
from src.features.soqm_components.repositories.components_repository import (
    ComponentRepository,
)
from src.features.quality_objectives.domain.objective import Objective
from src.features.soqm_components.domain.component import SOQMComponent
from src.features.quality_objectives.enums.objective_states import ObjectiveState
from src.features.soqm_components.enums.soqm_component import ComponentState
from src.features.risks.enums.risk_states import RiskStatus
from src.core.exceptions import ValidationError, NotFoundError


class RiskService:
    def __init__(
        self,
        repo,
        objective_repo: ObjectiveRepository,
        component_repo: ComponentRepository,
    ):
        self.repo = repo
        self.objective_repo: ObjectiveRepository = objective_repo
        self.component_repo: ComponentRepository = component_repo

    async def list(self):
        return

    async def create_risk(self, entity: Risk) -> Risk:

        component: SOQMComponent | None = await self.component_repo.get_by_id(
            entity.component_id
        )

        if not component:
            raise NotFoundError(
                message=f"No SOQM Component with ID {entity.component_id} was found",
            )

        if component.status != ComponentState.ACTIVE.value:
            raise ValidationError(
                message="Cannot use a non ACTIVE SOQM Component",
            )

        objective: Objective | None = await self.objective_repo.get_by_id(
            entity.objective_id
        )

        if not objective:
            raise NotFoundError(
                message=f"No Objective with ID {entity.objective_id} was found",
            )

        return

    async def get_risk_by_id(self):
        return

    async def update(self):
        return

    async def delete(self):
        return
