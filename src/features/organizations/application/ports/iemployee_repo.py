from abc import ABC, abstractmethod
from uuid import UUID

from src.features.organizations.domain.entities import Employee


class IEmployeeRepository(ABC):
    @abstractmethod
    async def save(self, employee: Employee) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get(self, employee_id: UUID) -> Employee | None:
        raise NotImplementedError()
