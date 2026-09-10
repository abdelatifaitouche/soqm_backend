from uuid import UUID
from src.features.soqm_engine.domain.entities.objective import Objective
from src.features.soqm_engine.infra.models import QualityObjective as ObjectiveDB
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select
from src.features.soqm_engine.application.ports import IObjectiveRepository


class ObjectiveRepository(IObjectiveRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, objective: Objective) -> None:
        insert_stmt = insert(ObjectiveDB).values(
            {
                "id": objective.id,
                "description": objective.description,
                "status": objective.status,
                "review_date": objective.review_date,
                "component_id": objective.component_id,
                "objective_reference": objective.objective_reference,
                "updated_at": objective.updated_at,
                "created_at": objective.created_at,
            }
        )

        upsert_stmt = insert_stmt.on_conflict_do_update(
            index_elements=["id"],
            set_={
                "description": objective.description,
                "status": objective.status,
                "review_date": objective.review_date,
                "component_id": objective.component_id,
                "objective_reference": objective.objective_reference,
                "updated_at": objective.updated_at,
                "lock_version": ObjectiveDB.lock_version + 1,
            },
            where=(ObjectiveDB.lock_version == objective.lock_version),
        )

        result = await self.session.execute(upsert_stmt)

        return result.rowcount > 0

    async def get(self, objective_id: UUID) -> Objective | None:
        stmt = select(ObjectiveDB).where(ObjectiveDB.id == objective_id)

        objective = (await self.session.execute(stmt)).scalar_one_or_none()

        if not objective:
            return None

        return Objective(
            id=objective.id,
            status=objective.status,
            description=objective.description,
            review_date=objective.review_date,
            component_id=objective.component_id,
            objective_reference=objective.objective_reference,
            updated_at=objective.updated_at,
            created_at=objective.created_at,
            lock_version=objective.lock_version,
        )

    async def delete(self, objective_id: UUID) -> None:
        pass
