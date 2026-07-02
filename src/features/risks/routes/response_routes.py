from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.infra.db.uow import get_db
from src.features.auth.security.dependencies import require_auth, require_permissions
from uuid import UUID
from src.features.risks.repositories.risk_response_repository import (
    RiskResponseRepository,
)
from src.features.risks.repositories.risk_repository import RiskRepository
from src.features.risks.services.response_service import ResponseService
from src.core.pagination import Pagination
from src.features.risks.schemas.risk_response import (
    RiskSummary,
    Response,
    RiskResponse,
    CreateRiskResponse,
)
from src.features.risks.filters.response_filters import ResponseFilters
from src.features.organizations.repositories.employee_repository import (
    EmployeeRepository,
)
from src.features.soqm_components.repositories.components_repository import (
    ComponentRepository,
)


def get_service(db: AsyncSession = Depends(get_db)) -> ResponseService:
    risk_repo: RiskRepository = RiskRepository(db)
    response_repo: RiskResponseRepository = RiskResponseRepository(db)
    employee_repo: EmployeeRepository = EmployeeRepository(db)
    component_repo: ComponentRepository = ComponentRepository(db)
    return ResponseService(response_repo, risk_repo, component_repo, employee_repo)


router = APIRouter(prefix="/responses")


@router.get("")
async def list(
    pagination: Pagination = Depends(),
    filters: ResponseFilters = Depends(),
    user=Depends(require_auth),
    service: ResponseService = Depends(
        get_service,
    ),
):
    responses = await service.list(pagination, filters)
    return [Response.model_validate(resp) for resp in responses]


@router.post("/")
async def create_response(
    data: CreateRiskResponse,
    user=Depends(require_auth),
    service: ResponseService = Depends(get_service),
):
    response = await service.create_response(user.get("sub"), data)
    return RiskResponse.model_validate(response)


@router.get("/{response_id}")
async def get_by_id(
    response_id: UUID,
    creds=Depends(require_auth),
    service: ResponseService = Depends(get_service),
):
    response = await service.get_by_id(response_id)
    return RiskResponse.model_validate(response)
