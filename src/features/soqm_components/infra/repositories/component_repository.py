from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from src.features.soqm_components.application.ports.component_repository import (
    IComponentRepository,
)
from src.features.soqm_components.domain.component import SOQMComponent as Component
from src.features.soqm_components.infra.models.soqm_component import (
    SOQMComponent as ComponentDB,
)


class ComponentRepository(IComponentRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_domain(self, orm: ComponentDB) -> Component:
        return Component(
            id=orm.id,
            name=orm.name,
            isqm_reference=orm.isqm_reference,
            status=orm.status,
            display_order=orm.display_order,
            description=orm.description,
        )

    async def save(self, component: Component) -> None:
        """UPSERT USING PG DIALECT"""

        component_data = {
            "id": component.id,
            "name": component.name,
            "isqm_reference": component.isqm_reference,
            "status": component.status,
            "description": component.description,
            "display_order": component.display_order,
        }

        stmt = insert(ComponentDB).values(component_data)

        upsert = stmt.on_conflict_do_update(
            index_elements=["id"],
            set_={
                "name": stmt.excluded.name,
                "isqm_reference": stmt.excluded.isqm_reference,
                "status": stmt.excluded.status,
                "description": stmt.excluded.description,
                "display_order": stmt.excluded.display_order,
            },
        )

        await self.session.execute(upsert)

    async def get(self, component_id: UUID) -> Component | None:
        stmt = select(ComponentDB).where(ComponentDB.id == component_id)

        component: ComponentDB | None = (
            await self.session.execute(stmt)
        ).scalar_one_or_none()

        if not component:
            return None

        return self._to_domain(component)

    async def delete(self, component_id: UUID) -> None:
        pass
