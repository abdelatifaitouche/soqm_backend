from dataclasses import asdict
from uuid import UUID

from src.core.exceptions import NotFoundError, ValidationError
from src.core.shared.interfaces.unit_of_work import IUnitOfWork
from src.features.soqm_engine.application.dtos.risk_dtos import CreateRisk, RiskUpdate
from src.features.soqm_engine.application.ports import (
    IComponentRepository,
    IObjectiveRepository,
    IRiskRepository,
    ISeqRepository,
)
from src.features.soqm_engine.domain.entities import Objective, Risk, SOQMComponent
from src.features.soqm_engine.domain.enums.component_state import ComponentState


class RiskUC:
    def __init__(
        self,
        uow: IUnitOfWork,
        risk_repository: IRiskRepository,
        seq_repo: ISeqRepository,
        component_repo: IComponentRepository,
        objective_repo: IObjectiveRepository,
    ):
        self.risk_repository = risk_repository
        self.uow = uow
        self.seq_repo = seq_repo
        self.component_repo = component_repo
        self.objective_repo = objective_repo

    async def _ensure_component_valide(self, component_id: UUID) -> int:
        component: SOQMComponent | None = await self.component_repo.get(component_id)

        if not component:
            raise NotFoundError(
                message=f"No SOQM Component with ID {component_id} was found",
            )

        if component.status != ComponentState.ACTIVE.value:
            raise ValidationError(
                message="Cannot use a non ACTIVE SOQM Component",
            )
        return component.display_order

    async def _ensure_objective_valide(self, objective_id: UUID):
        objective: Objective | None = await self.objective_repo.get(objective_id)

        if not objective:
            raise NotFoundError(
                message=f"No Objective with ID {objective_id} was found",
            )

    async def create_risk(self, user_id: UUID, data: CreateRisk) -> Risk:
        async with self.uow:
            component_order: int = await self._ensure_component_valide(
                data.component_id
            )

            sequence: int = await self.seq_repo.get_next_risk_seq(data.component_id)

            risk: Risk = Risk.create(
                objectives=data.objectives,
                component_id=data.component_id,
                sequence=sequence,
                component_idx=component_order,
                risk_description=data.risk_description,
                created_by=user_id,
                next_review_date=data.next_review_date,
                occurence=data.occurence,
                significance=data.significance,
            )

            await self.risk_repository.save(risk)

        return risk

    async def get(self, risk_id: UUID):
        risk = await self.risk_repository.get(risk_id)

        if not risk:
            raise NotFoundError(f"No Risk Found with id {risk_id}")

        return risk

    async def update_risk(self, risk_id: UUID, data: RiskUpdate):

        async with self.uow:
            update_data = asdict(data)

            risk = await self.get(risk_id)

            risk.update(**update_data)

            await self.risk_repository.save(risk)

        return risk

    async def add_objective(self, risk_id: UUID, objective_id: UUID):
        async with self.uow:
            risk = await self.get(risk_id)

            risk.add_objective(objective_id)

            await self.risk_repository.save(risk)

    async def remove_objective(self, risk_id: UUID, objective_id: UUID):
        async with self.uow:
            risk = await self.get(risk_id)

            risk.remove_objective(objective_id)

            await self.risk_repository.save(risk)

    async def add_response(self, risk_id: UUID, response_id: UUID):
        async with self.uow:
            risk = await self.get(risk_id)

            risk.add_response(response_id)

            await self.risk_repository.save(risk)

    async def remove_response(self, risk_id: UUID, response_id: UUID):
        async with self.uow:
            risk = await self.get(risk_id)

            risk.remove_response(response_id)

            await self.risk_repository.save(risk)

    async def delete(self, risk_id):
        """to be done later"""
        async with self.uow:
            risk = await self.risk_repository.get(risk_id)

            if not risk:
                raise NotFoundError("Risk Not Found")

            await self.risk_repository.delete(risk_id)

        return
