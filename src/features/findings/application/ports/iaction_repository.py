from abc import ABC, abstractmethod
from src.features.findings.domain.entities import Action
from uuid import UUID


class IActionRepository(ABC):
    @abstractmethod
    async def save(self, action: Action) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get(self, action_id: UUID) -> Action | None:
        raise NotImplementedError()
