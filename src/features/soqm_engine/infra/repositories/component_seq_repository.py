from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.features.soqm_engine.application.ports import ISeqRepository
from src.features.soqm_engine.infra.models import (
    ComponentObjectiveSeq,
    ComponentResponseSeq,
    ComponentRiskSequence,
)


class SequenceRepository(ISeqRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _inc_and_get(self, db_model, component_id: UUID):
        insert_stmt = insert(db_model).values(
            component_id=component_id,
            sequence=1,
            last_generated_at=datetime.now(),
        )

        upsert_stmt = insert_stmt.on_conflict_do_update(
            index_elements=["component_id"],
            set_={
                "sequence": db_model.sequence + 1,
                "last_generated_at": datetime.now(),
            },
        ).returning(db_model.sequence)

        next_seq = (await self.session.execute(upsert_stmt)).scalar_one()

        return next_seq

    async def get_next_objective_seq(self, component_id: UUID) -> int:
        return await self._inc_and_get(ComponentObjectiveSeq, component_id)

    async def get_next_response_seq(self, component_id: UUID) -> int:
        return await self._inc_and_get(ComponentResponseSeq, component_id)

    async def get_next_risk_seq(self, component_id: UUID) -> int:
        return await self._inc_and_get(ComponentRiskSequence, component_id)
