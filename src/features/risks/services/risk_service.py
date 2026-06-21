from uuid import UUID
from src.features.risks.domain.risk import Risk
from src.features.quality_objectives.repository.objective_repository import (
    ObjectiveRepository,
)
from src.features.soqm_components.repositories.components_repository import (
    ComponentRepository,
)
from src.features.risks.repositories.risk_repository import RiskRepository
from src.features.quality_objectives.domain.objective import Objective
from src.features.soqm_components.domain.component import SOQMComponent
from src.features.quality_objectives.enums.objective_states import ObjectiveState
from src.features.soqm_components.enums.soqm_component import ComponentState
from src.features.risks.enums.risk_states import RiskStatus
from src.core.exceptions import ValidationError, NotFoundError
from datetime import date
from src.features.risks.schemas.risk import CreateRisk, UpdateRisk
from src.features.risks.repositories.risk_response_repository import (
    RiskResponseRepository,
)
from src.features.risks.domain.risk_response import RiskResponse as RiskResponseEntity


class RiskService:
    def __init__(
        self,
        repo: RiskRepository,
        objective_repo: ObjectiveRepository,
        component_repo: ComponentRepository,
    ):
        self.repo: RiskRepository = repo
        self.objective_repo: ObjectiveRepository = objective_repo
        self.component_repo: ComponentRepository = component_repo

    async def list(self, pagination, filters):
        return await self.repo.list(pagination, filters)

    async def _ensure_component_valide(self, component_id: UUID):
        component: SOQMComponent | None = await self.component_repo.get_by_id(
            component_id
        )

        if not component:
            raise NotFoundError(
                message=f"No SOQM Component with ID {component_id} was found",
            )

        if component.status != ComponentState.ACTIVE.value:
            raise ValidationError(
                message="Cannot use a non ACTIVE SOQM Component",
            )

    async def _ensure_objective_valide(self, objective_id: UUID):
        objective: Objective | None = await self.objective_repo.get_by_id(objective_id)

        if not objective:
            raise NotFoundError(
                message=f"No Objective with ID {objective_id} was found",
            )

    async def create_risk(self, user_id: UUID, data: CreateRisk) -> Risk:

        risk: Risk = Risk.create(
            objective_id=data.objective_id,
            component_id=data.component_id,
            risk_ref=data.risk_ref,
            risk_discription=data.risk_discription,
            created_by=user_id,
            next_review_date=data.next_review_date,
            occurence=data.occurence,
            significance=data.significance,
        )

        await self._ensure_component_valide(risk.component_id)
        await self._ensure_objective_valide(risk.objective_id)

        return await self.repo.create(risk)

    async def get_risk_by_id(self, entity_id: UUID):
        risk: Risk | None = await self.repo.get_by_id(entity_id)

        if not risk:
            raise NotFoundError(message=f"Risk with ID {entity_id} was not found")

        return risk

    async def assess_risk(self, user_id: UUID, entity_id: UUID):
        """
        SAME CODE IS DUPLICATED IN THREE DIFFERENT METHODS

        We can refactor this later by introducing lambda fuunction on the get_by_d and save()
        """
        risk: Risk = await self.get_risk_by_id(entity_id)
        risk.assess()
        return await self.repo.update(risk)

    async def plan_treatment(self, user_id: UUID, entity_id: UUID):
        risk: Risk = await self.get_risk_by_id(entity_id)

        risk.plan_treatment()

        return await self.repo.update(risk)

    async def close_risk(self, user_id: UUID, entity_id: UUID):
        risk: Risk = await self.get_risk_by_id(entity_id)
        risk.close()
        return await self.repo.update(risk)

    async def update(self, user_id: UUID, entity_id: UUID, data: UpdateRisk):

        risk: Risk = await self.get_risk_by_id(entity_id)

        risk.update(
            risk_ref=data.risk_ref,
            risk_discreption=data.risk_discription,
            next_review_date=data.next_review_date,
            occurence=data.occurence,
            significance=data.significance,
        )

        return await self.repo.update(risk)

    async def list_risks_by_objective(self, objective_id: UUID):
        return await self.repo.list_by_objective(objective_id)

    async def delete(self):
        return
