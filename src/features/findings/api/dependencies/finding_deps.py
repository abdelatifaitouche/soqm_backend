from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps.db_session import get_db
from src.features.findings.application.usecases.finding_uc import FindingUC
from src.features.findings.infra.queries.finding_queries import FindingQueryService
from src.features.findings.infra.repositories.finding_dept_seq import (
    FindingDeptSequenceRepository,
)
from src.features.findings.infra.repositories.finding_repository import (
    FindingRepository,
)
from src.features.organizations.infra.repositories import DepartmentRepository
from src.infra.db.unit_of_work import UnitOfWork


def get_finding_queries(db: AsyncSession = Depends(get_db)) -> FindingQueryService:
    return FindingQueryService(db)


def get_finding_uc(db: AsyncSession = Depends(get_db)) -> FindingUC:
    uow = UnitOfWork(db)
    repo = FindingRepository(db)
    dept_repo = DepartmentRepository(db)
    seq_repo = FindingDeptSequenceRepository(db)
    return FindingUC(
        uow=uow,
        repo=repo,
        seq_repo=seq_repo,
        dept_repo=dept_repo,
    )
