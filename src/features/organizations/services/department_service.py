from uuid import UUID
from src.features.organizations.repositories.department_repository import (
    DepartmentRepository,
)
from src.features.organizations.domain.department import Department as Entity


class DepartmentService:
    def __init__(self, repo: DepartmentRepository):
        self.repo: DepartmentRepository = repo

    async def list(self):
        return await self.repo.list()

    async def create(self, data: Entity) -> Entity:
        return await self.repo.save(data)

    async def get_by_id(self, entity_id: UUID):
        return await self.repo.get_by_id(entity_id)
