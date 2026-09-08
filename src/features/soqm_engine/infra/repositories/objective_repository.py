from uuid import UUID
from src.features.soqm_engine.domain.entities.objective import Objective
from sqlalchemy.ext.asyncio import AsyncSession
from src.features.soqm_engine.application.ports.iobjective_repo import (
    IObjectiveRepository,
)


class ObjectiveRepository(IObjectiveRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, objective: Objective) -> None:
        pass

    async def get(self, objective_id: UUID) -> Objective | None:
        pass

    async def delete(self, objective_id: UUID) -> None:
        pass
