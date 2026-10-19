from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.deps.db_session import get_db
from src.features.findings.application.usecases import ActionUC
from src.features.findings.infra.repositories import ActionRepository, FindingRepository
from src.infra.db.unit_of_work import UnitOfWork
from src.features.findings.infra.queries import ActionQueryService


async def get_action_uc(db: AsyncSession = Depends(get_db)) -> ActionUC:
    uow = UnitOfWork(db)
    repo = ActionRepository(db)
    finding_repo = FindingRepository(db)
    return ActionUC(uow, repo, finding_repo)


async def get_action_queries(db: AsyncSession = Depends(get_db)) -> ActionQueryService:
    return ActionQueryService(db)
