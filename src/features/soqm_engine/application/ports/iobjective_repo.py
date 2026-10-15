from abc import ABC, abstractmethod
from uuid import UUID

from src.features.soqm_engine.domain.entities.objective import Objective


class IObjectiveRepository(ABC):
    @abstractmethod
    async def get(self, objective_id: UUID) -> Objective | None:
        raise NotImplementedError()

    @abstractmethod
    async def save(self, objective: Objective) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, objective_id: UUID) -> None:
        raise NotImplementedError()
