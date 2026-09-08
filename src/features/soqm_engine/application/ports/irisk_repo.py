from abc import ABC, abstractmethod
from uuid import UUID
from src.features.soqm_engine.domain.entities.risk import Risk


class IRiskRepository(ABC):
    @abstractmethod
    async def get(self, risk_id: UUID) -> Risk | None:
        raise NotImplementedError()

    @abstractmethod
    async def save(self, risk: Risk) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, risk_id: UUID) -> None:
        raise NotImplementedError()
