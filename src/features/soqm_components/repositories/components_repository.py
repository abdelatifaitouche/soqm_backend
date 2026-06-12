from src.core.repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from sqlalchemy import select, delete, update
from src.features.soqm_components.models.soqm_component import SOQMComponent
from src.features.soqm_components.domain.component import (
    SOQMComponent as ComponentEntity,
    CreateComponent,
)


class ComponentRepository(BaseRepository):
    model = SOQMComponent

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    def _to_domain(self, orm: SOQMComponent) -> ComponentEntity:
        return ComponentEntity(
            id=orm.id,
            name=orm.name,
            isqm_reference=orm.isqm_reference,
            status=orm.status,
            display_order=orm.display_order,
            description=orm.description,
        )

    def _apply_filters(self, stmt):
        return stmt

    async def list(self) -> list[ComponentEntity]:
        stmt = select(self.model)

        stmt = self._apply_filters(stmt)

        result = await self.db.execute(stmt)

        data = result.scalars().all()

        return [self._to_domain(d) for d in data]

    def _to_orm(self, entity: CreateComponent):
        return self.model(
            name=entity.name,
            description=entity.description,
            isqm_reference=entity.isqm_reference,
            display_order=entity.display_order,
        )

    async def save(self, entity):
        try:
            orm = self._to_orm(entity)
            self.db.add(orm)
            await self.db.flush()
            await self.db.refresh(orm)
            return self._to_domain(orm)
        except Exception as e:
            raise self._translate_db_errors(e)

    async def get_by_id(self, entity_id: UUID) -> ComponentEntity | None:
        stmt = select(self.model).where(self.model.id == entity_id)

        result = await self.db.execute(stmt)

        data = result.scalar_one_or_none()

        return self._to_domain(data) if data else None

    async def update(self, entity: ComponentEntity) -> ComponentEntity:
        try:
            await self.db.execute(
                update(self.model)
                .where(self.model.id == entity.id)
                .values(
                    name=entity.name,
                    status=entity.status,
                    isqm_reference=entity.isqm_reference,
                    description=entity.description,
                    display_order=entity.display_order,
                )
            )
            await self.db.flush()
            return entity
        except Exception as e:
            raise self._translate_db_errors(e)

    async def delete(self, entity_id: UUID):
        try:
            await self.db.execute(delete(self.model).where(self.model.id == entity_id))
        except Exception as e:
            raise self._translate_db_errors(e)
