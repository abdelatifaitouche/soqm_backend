from uuid import UUID
from sqlalchemy import select, Select
from sqlalchemy.ext.asyncio import AsyncSession
from src.features.soqm_components.application.dtos.component_dto import (
    SOQMComponentDetails,
    SOQMComponentList,
)
from src.features.soqm_components.application.ports.component_query_service import (
    IComponentQueryService,
)
from src.features.soqm_components.infra.models.soqm_component import (
    SOQMComponent as SOQMComponentDB,
)
from src.features.soqm_components.application.dtos.filters import ComponentFilters
from typing import Any


class ComponentQueryService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_component_details(
        self, component_id: UUID
    ) -> SOQMComponentDetails | None:
        stmt = select(SOQMComponentDB).where(
            SOQMComponentDB.id == component_id,
        )

        result = (await self.session.execute(stmt)).scalar_one_or_none()

        return (
            SOQMComponentDetails(
                id=result.id,
                name=result.name,
                isqm_reference=result.isqm_reference,
                display_order=result.display_order,
                status=result.status,
                description=result.description,
            )
            if result
            else None
        )

    def _apply_filters(
        self, stmt: Select[Any], filters: ComponentFilters
    ) -> Select[Any]:
        if filters.status:
            stmt = stmt.where(SOQMComponentDB.status == filters.status)
        return stmt

    async def list(
        self, pagination, filters: ComponentFilters, ordering
    ) -> list[SOQMComponentList]:

        stmt = select(
            SOQMComponentDB.id,
            SOQMComponentDB.name,
            SOQMComponentDB.display_order,
            SOQMComponentDB.isqm_reference,
            SOQMComponentDB.status,
        )

        stmt = self._apply_filters(stmt, filters)

        components = (await self.session.execute(stmt)).mappings().all()

        return [
            SOQMComponentList(
                id=cp["id"],
                name=cp["name"],
                status=cp["status"],
                isqm_reference=cp["isqm_reference"],
                display_order=cp["display_order"],
            )
            for cp in components
        ]
