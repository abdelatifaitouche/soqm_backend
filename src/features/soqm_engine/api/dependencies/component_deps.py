from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.deps.db_session import get_db
from src.features.soqm_engine.application.usecases.component_uc import ComponentUC
from src.infra.db.unit_of_work import UnitOfWork
from src.features.soqm_engine.infra.repositories.component_repository import (
    ComponentRepository,
)
from src.features.soqm_engine.infra.queries.component_query_service import (
    ComponentQueryService,
)


def get_component_queries(db: AsyncSession = Depends(get_db)) -> ComponentQueryService:
    return ComponentQueryService(db)


def get_component_uc(db: AsyncSession = Depends(get_db)) -> ComponentUC:
    repo = ComponentRepository(db)
    uow = UnitOfWork(db)
    return ComponentUC(uow, repo)
