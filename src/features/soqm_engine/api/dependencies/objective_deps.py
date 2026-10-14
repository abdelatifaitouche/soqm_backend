from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.deps.db_session import get_db

from src.features.soqm_engine.application.usecases.objective_uc import ObjectiveUC
from src.features.soqm_engine.infra.repositories import (
    ObjectiveRepository,
    ComponentRepository,
    SequenceRepository,
)
from src.features.soqm_engine.infra.queries import ObjectiveQueryService

from src.infra.db.unit_of_work import UnitOfWork


def get_queries(
    db: AsyncSession = Depends(get_db),
) -> ObjectiveQueryService:
    return ObjectiveQueryService(db)


def get_objective_uc(db: AsyncSession = Depends(get_db)) -> ObjectiveUC:
    uow = UnitOfWork(db)
    objective_repo = ObjectiveRepository(db)
    component_repo = ComponentRepository(db)
    seq_repository = SequenceRepository(db)
    return ObjectiveUC(
        uow,
        objective_repo,
        component_repo,
        seq_repository,
    )
