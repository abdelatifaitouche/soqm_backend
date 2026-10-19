from abc import ABC, abstractmethod
from src.features.findings.domain.entities import RootCauseCategory


class IRcaTrackerRepository(ABC):
    @abstractmethod
    async def bulk_insert(self, categories: list[RootCauseCategory]):
        raise NotImplementedError()
