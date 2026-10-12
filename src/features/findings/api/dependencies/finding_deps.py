from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.deps.db_session import get_db
from src.features.findings.application.usecases.finding_uc import FindingUC
from src.infra.db.unit_of_work import UnitOfWork
from src.features.findings.infra.repositories.finding_repository import (
    FindingRepository,
)
from src.features.findings.infra.queries.finding_queries import FindingQueryService


def get_finding_queries(db: AsyncSession = Depends(get_db)) -> FindingQueryService:
    return FindingQueryService(db)


def get_finding_uc(db: AsyncSession = Depends(get_db)) -> FindingUC:
    uow = UnitOfWork(db)
    repo = FindingRepository(db)
    return FindingUC(uow, repo)
