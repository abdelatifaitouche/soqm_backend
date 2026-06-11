from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from src.features.organizations.domain.department import (
    Department as Entity,
    DeptCompact,
)
from src.features.organizations.models.department import Department as DepartmentDB


class DepartmentRepository:
    model = DepartmentDB

    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def save(self, entity: Entity) -> Entity:
        orm: DepartmentDB = DepartmentDB(name=entity.name)

        if entity.parent_dept:
            orm.parent_id = entity.parent_dept

        self.db.add(orm)
        await self.db.flush()
        await self.db.refresh(orm)

        return Entity(
            id=orm.id,
            name=orm.name,
            parent_dept=orm.parent_id,
        )

    async def list(self) -> list[Entity]:
        stmt = select(self.model)

        result = await self.db.execute(stmt)

        data = result.scalars().all()
        return [
            Entity(
                id=dept.id,
                name=dept.name,
                parent_dept=dept.parent_id,
            )
            for dept in data
        ]

    async def get_by_id(self, entity_id: UUID) -> Entity | None:
        stmt = (
            select(self.model)
            .where(self.model.id == entity_id)
            .options(
                selectinload(
                    self.model.children,
                ),
            )
        )

        result = await self.db.execute(stmt)

        data = result.scalar_one_or_none()

        if not data:
            return None

        return Entity(
            name=data.name,
            parent_dept=data.parent_id,
            id=data.id,
            children_dept=[
                DeptCompact(id=dep.id, name=dep.name) for dep in data.children
            ]
            if data.children
            else [],
        )
