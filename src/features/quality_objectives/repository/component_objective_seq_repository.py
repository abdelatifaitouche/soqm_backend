from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.features.quality_objectives.models.component_objective_seq import (
    ComponentObjectiveSeq,
)
from uuid import UUID
from datetime import datetime


class ComponentObjectiveSeqRepository:
    model = ComponentObjectiveSeq

    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_next_val(self, component_id: UUID) -> int:

        stmt = select(self.model).where(self.model.component_id == component_id)

        seq: ComponentObjectiveSeq | None = (
            await self.db.execute(stmt)
        ).scalar_one_or_none()

        if not seq:
            seq = ComponentObjectiveSeq(
                component_id=component_id,
                sequence=0,
            )

            self.db.add(seq)
            await self.db.flush()

        next_seq = seq.sequence + 1
        seq.sequence = next_seq
        seq.last_generated_at = datetime.now()

        await self.db.flush()

        return next_seq
