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
from src.features.risks.schemas.risk_response import RiskResponse, CreateRiskResponse


def get_service(db: AsyncSession = Depends(get_db)) -> ResponseService:
    risk_repo: RiskRepository = RiskRepository(db)
    response_repo: RiskResponseRepository = RiskResponseRepository(db)
    return ResponseService(response_repo, risk_repo)


router = APIRouter(prefix="/responses")


@router.get("")
async def list(
    risk_id: UUID,
    pagination: Pagination = Depends(),
    user=Depends(require_auth),
    service: ResponseService = Depends(
        get_service,
    ),
):
    responses = await service.list(risk_id, pagination)
    return [RiskResponse.model_validate(resp) for resp in responses]


@router.post("/{risk_id}/")
async def create_response(
    risk_id: UUID,
    data: CreateRiskResponse,
    user=Depends(require_auth),
    service: ResponseService = Depends(get_service),
):
    response = await service.create_response(risk_id, user.get("sub"), data)
    return RiskResponse.model_validate(response)


@router.get("/{response_id}")
async def get_by_id(risk_id: UUID, response_id: UUID, creds, service):
    return
