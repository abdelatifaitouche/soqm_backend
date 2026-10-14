from abc import ABC, abstractmethod
from uuid import UUID


class IFindingDeptSeqRepository(ABC):
    @abstractmethod
    async def inc_get(self, department_id: UUID):
        raise NotImplementedError()
