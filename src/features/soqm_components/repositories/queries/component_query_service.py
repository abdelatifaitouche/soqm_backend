from sqlalchemy.ext.asyncio import AsyncSession
from src.features.soqm_components.models.soqm_component import (
    SOQMComponent as SOQMComponentDB,
)
from sqlalchemy import select, Select
from uuid import UUID
from src.features.soqm_components.filters.filters import ComponentFilters
from src.features.soqm_components.services.dto import (
    SOQMComponentDetails,
    SOQMComponentList,
    SOQMComponentOption,
)
from typing import Any


class ComponentQueries:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_component_details(
        self, component_id: UUID
    ) -> SOQMComponentDetails | None:
        stmt = select(SOQMComponentDB).where(
            SOQMComponentDB.id == component_id,
        )

        result = (await self.db.execute(stmt)).scalar_one_or_none()

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

    async def list_options(self) -> list[SOQMComponentOption]:
        stmt = select(SOQMComponentDB.id, SOQMComponentDB.name)

        results = (await self.db.execute(stmt)).mappings().all()

        return (
            [
                SOQMComponentOption(
                    id=cp.id,
                    name=cp.name,
                )
                for cp in results
            ]
            if results
            else []
        )

    async def list(self, filters: ComponentFilters) -> list[SOQMComponentList]:
        stmt = select(SOQMComponentDB).order_by("display_order")

        stmt = self._apply_filters(stmt, filters)

        results = (await self.db.execute(stmt)).scalars().all()

        return [
            SOQMComponentList(
                id=cp.id,
                name=cp.name,
                status=cp.status,
                display_order=cp.display_order,
                isqm_reference=cp.isqm_reference,
            )
            for cp in results
        ]
