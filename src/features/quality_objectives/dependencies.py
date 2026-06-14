from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.infra.db.uow import get_db
from src.features.quality_objectives.services.objective_service import ObjectiveService
from src.features.quality_objectives.repository.objective_repository import (
    ObjectiveRepository,
)


def get_service(db: AsyncSession = Depends(get_db)) -> ObjectiveService:
    repo: ObjectiveRepository = ObjectiveRepository(db)
    return ObjectiveService(repo)
