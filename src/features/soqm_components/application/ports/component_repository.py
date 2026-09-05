from abc import ABC, abstractmethod
from uuid import UUID
from src.features.soqm_components.domain.component import SOQMComponent


class IComponentRepository(ABC):
    @abstractmethod
    async def get(self, component_id: UUID) -> SOQMComponent | None:
        raise NotImplementedError()

    @abstractmethod
    async def save(self, component: SOQMComponent) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, component_id: UUID) -> None:
        raise NotImplementedError()
