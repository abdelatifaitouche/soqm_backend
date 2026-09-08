from abc import ABC, abstractmethod
from uuid import UUID


class ISeqRepository(ABC):
    @abstractmethod
    async def get_next_objective_seq(self, component_id: UUID) -> int:
        raise NotImplementedError()

    @abstractmethod
    async def get_next_response_seq(self, component_id: UUID) -> int:
        raise NotImplementedError()

    @abstractmethod
    async def get_next_risk_seq(self, component_id: UUID) -> int:
        raise NotImplementedError()
