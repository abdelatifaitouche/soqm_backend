from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import Load, joinedload
from uuid import UUID
from src.features.soqm_engine.infra.models import (
    QualityObjective as ObjectiveDB,
    SOQMComponent as ComponentDB,
)
from src.features.soqm_engine.application.dtos.objective_dtos import (
    ObjectiveDetails,
    ObjectiveList,
)


class ObjectiveQueryService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(self) -> list[ObjectiveList]:
        stmt = select(
            ObjectiveDB.id,
            ObjectiveDB.objective_reference,
            ObjectiveDB.status,
            ObjectiveDB.review_date,
            ComponentDB.name.label("component_name"),
        ).join(ObjectiveDB.component)

        objectives = (await self.session.execute(stmt)).mappings().all()

        return [ObjectiveList(**obj) for obj in objectives]

    async def get_objective_details(
        self, objective_id: UUID
    ) -> ObjectiveDetails | None:
        stmt = select(
            ObjectiveDB.id,
            ObjectiveDB.objective_reference,
            ObjectiveDB.description,
            ObjectiveDB.review_date,
            ObjectiveDB.component_id,
            ObjectiveDB.created_at,
            ObjectiveDB.updated_at,
            ObjectiveDB.status,
        ).where(ObjectiveDB.id == objective_id)

        objective = (await self.session.execute(stmt)).mappings().fetchone()

        if not objective:
            return None

        return ObjectiveDetails(**objective)
