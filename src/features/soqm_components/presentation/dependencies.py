from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.deps.db_session import get_db
from src.infra.db.unit_of_work import UnitOfWork

from src.features.soqm_components.infra.repositories.component_repository import (
    ComponentRepository,
)
from src.features.soqm_components.application.usecases.component_usecases import (
    ComponentUC,
)
from src.features.soqm_components.infra.queries.component_query_service import (
    ComponentQueryService,
)


def get_uc(db: AsyncSession = Depends(get_db)):
    uow = UnitOfWork(db)
    component_repo = ComponentRepository(db)
    return ComponentUC(
        uow=uow,
        component_repo=component_repo,
    )


def get_query_service(db: AsyncSession = Depends(get_db)):
    return ComponentQueryService(db)
