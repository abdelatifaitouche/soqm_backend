from uuid import UUID
from src.core.shared.interfaces.unit_of_work import IUnitOfWork
from src.features.soqm_engine.application.ports import (
    IComponentRepository,
    IObjectiveRepository,
    ISeqRepository,
)
from src.features.soqm_engine.domain.entities import Objective, SOQMComponent
from src.features.soqm_engine.application.dtos.objective_dtos import CreateObjective
from src.features.soqm_engine.domain.services.objective_ref_generator import (
    ObjectiveRefGenerator,
)
from src.core.exceptions import NotFoundError


class ObjectiveUC:
    def __init__(
        self,
        uow: IUnitOfWork,
        objective_repo: IObjectiveRepository,
        component_repo: IComponentRepository,
        sequence_repository: ISeqRepository,
    ):
        self.objective_repo = objective_repo
        self.component_repo = component_repo
        self.sequence_repository = sequence_repository
        self.uow = uow

    async def _generate_objective_reference(self, component: SOQMComponent) -> str:
        """
        CALL THIS METHODS INSIDE A UNIT OF A WORK
        """

        next_seq: int = await self.sequence_repository.get_next_objective_seq(
            component.id
        )

        seq: str = ObjectiveRefGenerator.generate_objective_ref(
            component.display_order, next_seq
        )

        return seq

    async def create(self, data: CreateObjective) -> Objective:
        async with self.uow:
            component: SOQMComponent | None = await self.component_repo.get(
                data.component_id
            )

            if not component:
                raise NotFoundError(
                    message=f"Component with {data.component_id} was not found",
                )
            component.ensure_can_add_objectives()

            seq: str = await self._generate_objective_reference(component)

            entity = Objective.create(
                description=data.description,
                review_date=data.review_date,
                objective_reference=seq,
                component_id=component.id,
            )

            await self.objective_repo.save(entity)
        return entity

    async def approve(self, objective_id: UUID):
        async with self.uow:
            objective = await self.objective_repo.get(objective_id)

            if not objective:
                raise NotFoundError("Objective not found")

            objective.approve()

            result = await self.objective_repo.save(objective)

            if not result:
                raise Exception("Saving error some where need to check")

        return result
