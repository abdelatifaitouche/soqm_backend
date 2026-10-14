from abc import ABC, abstractmethod
from uuid import UUID
from src.features.soqm_engine.domain.entities.response import RiskResponse as Response


class IResponseRepository(ABC):
    @abstractmethod
    async def get(self, response_id: UUID) -> Response | None:
        raise NotImplementedError()

    @abstractmethod
    async def save(self, response: Response) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, response_id: UUID) -> None:
        raise NotImplementedError()
