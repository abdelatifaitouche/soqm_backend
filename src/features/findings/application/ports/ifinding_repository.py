from abc import ABC, abstractmethod
from uuid import UUID

from src.features.findings.domain.entities.finding import Finding


class IFindingRepository(ABC):
    @abstractmethod
    async def save(self, finding: Finding) -> None:
        pass

    @abstractmethod
    async def get(self, finding_id: UUID) -> Finding | None:
        raise NotImplementedError()
