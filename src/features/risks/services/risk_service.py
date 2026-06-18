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

    async def create_risk(self, entity: Risk) -> Risk:
        if entity.occurence <= 0 or entity.occurence > 3:
            raise ValidationError(
                message="Occurence must be between 1 AND 3",
                details={
                    "occurence": entity.occurence,
                },
            )
        if entity.significance <= 0 or entity.significance > 3:
            raise ValidationError(
                message="Significance must be between 1 AND 3",
                details={
                    "significance": entity.significance,
                },
            )

        if entity.date_identified > date.today():
            raise ValidationError(
                message="cannot identify in the future,",
            )

        if entity.next_review_date:
            if entity.next_review_date <= date.today():
                raise ValidationError(
                    message="next review date must be in the future",
                    details={
                        "next_review_date": entity.next_review_date,
                    },
                )

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

        entity: Risk = entity.calculate_score()

        return await self.repo.create(entity)

    async def get_risk_by_id(self, entity_id: UUID):
        risk: Risk | None = await self.repo.get_by_id(entity_id)

        if not risk:
            raise NotFoundError(message=f"Risk with ID {entity_id} was not found")

        return risk

    async def update(self):
        return

    async def delete(self):
        return
