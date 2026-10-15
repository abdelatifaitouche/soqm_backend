from dataclasses import asdict
from uuid import UUID

from src.core.exceptions import NotFoundError, ValidationError
from src.core.shared.interfaces.unit_of_work import IUnitOfWork
from src.features.organizations.repositories.employee_repository import (
    EmployeeRepository,
)
from src.features.soqm_engine.application.dtos.response_dtos import (
    CreateRiskResponse,
    UpdateRiskResponse,
)
from src.features.soqm_engine.application.ports import (
    IComponentRepository,
    IResponseRepository,
    ISeqRepository,
)
from src.features.soqm_engine.domain.entities.response import RiskResponse
from src.features.soqm_engine.domain.services.response_ref_gen import (
    ResponseRefGenerator,
)


class ResponseUC:
    def __init__(
        self,
        uow: IUnitOfWork,
        response_repo: IResponseRepository,
        seq_repo: ISeqRepository,
        component_repo: IComponentRepository,
        employee_repo: EmployeeRepository,
    ):
        self.response_repo = response_repo
        self.uow = uow
        self.seq_repo = seq_repo
        self.component_repo = component_repo
        self.employee_repo = employee_repo

    async def _get_active_employee(self, employee_id: UUID):
        owner = await self.employee_repo.get_by_id(employee_id)

        if not owner:
            raise NotFoundError(
                message=f"Employee with ID {employee_id} was not found",
            )

        if owner.status in (
            "IN_ACTIVE",
            "TERMINATED",
        ):
            raise ValidationError(
                message=f"Employee choosen is not active",
                details={"status": owner.status},
            )
        return owner

    async def _get_valid_component(self, component_id: UUID):
        component = await self.component_repo.get(component_id)

        if not component:
            raise NotFoundError(
                message=f"ISQM Component with {component_id} not found,",
            )

        if component.status != "ACTIVE":
            raise ValidationError(
                message="ISQM Component is not active",
            )

        return component

    async def create_response(self, user: UUID, data: CreateRiskResponse):
        async with self.uow:
            component = await self._get_valid_component(data.component_id)

            sequence: int = await self.seq_repo.get_next_response_seq(data.component_id)

            response_ref: str = ResponseRefGenerator.generate(component.name, sequence)

            owner = await self._get_active_employee(data.response_employee)

            response = RiskResponse.create(
                response_ref=response_ref,
                component_id=component.id,
                risks=data.risks,
                response_name=data.response_name,
                response_description=data.response_description,
                response_type=data.response_type,
                date_implementation=data.date_implementation,
                frequency=data.frequency,
                execution_type=data.execution_type,
                evidence_notes=data.evidence_notes,
                date_monitored_design=data.date_monitored_design,
                date_monitored_operating=data.date_monitored_operating,
                owner=owner.id,
                created_by=user,
            )

            await self.response_repo.save(response)

    async def update_response(self, response_id: UUID, data: UpdateRiskResponse):
        async with self.uow:
            response = await self.response_repo.get(response_id)

            if not response:
                raise NotFoundError("Cannot find response")

            response.update(
                response_name=data.response_name,
                response_description=data.response_description,
                response_type=data.response_type,
                frequency=data.frequency,
                execution_type=data.execution_type,
            )

            await self.response_repo.save(response)

    async def remove_risk(self, response_id: UUID, risk_id: UUID):
        async with self.uow:
            response = await self.response_repo.get(response_id)

            if not response:
                raise NotFoundError("Cannot find response")

            response.remove_risk(risk_id)

            await self.response_repo.save(response)

    async def add_risk(self, response_id: UUID, risk_id: UUID):
        async with self.uow:
            response = await self.response_repo.get(response_id)

            if not response:
                raise NotFoundError("Cannot find response")

            response.add_risk(risk_id)

            await self.response_repo.save(response)
