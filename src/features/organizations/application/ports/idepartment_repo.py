from abc import ABC, abstractmethod
from src.features.organizations.domain.entities import Department
from uuid import UUID


class IDepartmentRepository(ABC):
    @abstractmethod
    async def save(self, department: Department) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get(self, department_id: UUID) -> Department | None:
        raise NotImplementedError()
