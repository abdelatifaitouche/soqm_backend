from src.features.risks.repositories.risk_response_repository import (
    RiskResponseRepository,
)
from src.features.risks.domain.risk_response import RiskResponse as ResponseEntity
from src.features.risks.schemas.risk_response import CreateRiskResponse, RiskResponse
from src.features.risks.repositories.risk_repository import RiskRepository
from uuid import UUID
from src.core.exceptions import NotFoundError, ValidationError
from src.core.pagination import Pagination
from src.features.risks.filters.response_filters import ResponseFilters
from src.features.risks.enums.risk_states import RiskStatus
from src.features.risks.domain.response_ref_generator import ResponseRefGenerator
from src.features.risks.repositories.component_response_seq_repository import (
    ComponentResponseSeqRepository,
)
from src.features.soqm_components.repositories.components_repository import (
    ComponentRepository,
)
from src.features.soqm_components.domain.component import SOQMComponent
from src.features.organizations.repositories.employee_repository import (
    EmployeeRepository,
)
from src.features.organizations.domain.employee import Employee


class ResponseService:
    def __init__(
        self,
        repo: RiskResponseRepository,
        risk_repo: RiskRepository,
        component_repo: ComponentRepository,
        employee_repo: EmployeeRepository,
    ):
        self.repo: RiskResponseRepository = repo
        self.risk_repo: RiskRepository = risk_repo
        self.seq_repo: ComponentResponseSeqRepository = ComponentResponseSeqRepository(
            self.repo.db
        )
        self.component_repo: ComponentRepository = component_repo
        self.employee_repo: EmployeeRepository = employee_repo

    async def _get_active_employee(self, employee_id: UUID) -> Employee:
        owner: Employee | None = await self.employee_repo.get_by_id(employee_id)

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

    async def _get_valid_component(self, component_id: UUID) -> SOQMComponent:
        component: SOQMComponent | None = await self.component_repo.get_by_id(
            component_id
        )

        if not component:
            raise NotFoundError(
                message=f"ISQM Component with {component_id} not found,",
            )

        if component.status != "ACTIVE":
            raise ValidationError(
                message="ISQM Component is not active",
            )

        return component

    async def create_response(
        self, user_id: UUID, data: CreateRiskResponse
    ) -> ResponseEntity:

        component: SOQMComponent = await self._get_valid_component(data.component_id)
        owner: Employee = await self._get_active_employee(data.response_employee)

        sequence: int = await self.seq_repo.get_next_val(data.component_id)

        response_ref: str = ResponseRefGenerator.generate(component.name, sequence)

        response: ResponseEntity = ResponseEntity.response_create(
            risks=data.risks,
            response_name=data.response_name,
            response_ref=response_ref,
            component_id=component.id,
            response_description=data.response_description,
            evidence_notes=data.evidence_notes,
            response_type=data.response_type,
            created_by=user_id,
            owner=data.response_employee,
            date_implementation=data.date_implementation,
            date_monitored_design=data.date_monitored_design,
            date_monitored_operating=data.date_monitored_operating,
            frequency=data.frequency.value,
            execution_type=data.execution_type.value,
        )
        # this will emit an event here to be logged or notify (NOT IMPLEMENTED YET)
        return await self.repo.create(response)

    async def get_by_id(self, entity_id: UUID) -> ResponseEntity:

        response: ResponseEntity | None = await self.repo.get_by_id(entity_id)

        if not response:
            raise NotFoundError(
                message=f"Response with ID {entity_id} was not found",
            )

        return response
