from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.features.soqm_components.models.soqm_component import SOQMComponent
from src.features.soqm_components.domain.component import (
    SOQMComponent as ComponentEntity,
)


class ComponentRepository:
    model = SOQMComponent

    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    def _to_domain(self, orm: SOQMComponent) -> ComponentEntity:
        return ComponentEntity(
            id=orm.id, name=orm.name, isqm_reference=orm.isqm_reference
        )

    def _apply_filters(self, stmt):
        return stmt

    async def list(self) -> list[ComponentEntity]:
        stmt = select(self.model)

        stmt = self._apply_filters(stmt)

        result = await self.db.execute(stmt)

        data = result.scalars().all()

        return [self._to_domain(d) for d in data]
