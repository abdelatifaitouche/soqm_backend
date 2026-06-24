from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.features.risks.models.component_risk_seq import ComponentRiskSequence
from sqlalchemy import select
from datetime import datetime


class ComponentRiskSeqRepository:
    model = ComponentRiskSequence

    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_next_val(self, component_id: UUID) -> int:
        stmt = select(self.model).where(self.model.component_id == component_id)

        seq = (await self.db.execute(stmt)).scalar_one_or_none()

        if not seq:
            seq = ComponentRiskSequence(
                component_id=component_id,
                sequence=0,
            )
            self.db.add(seq)
            await self.db.flush()

        next_val = seq.sequence + 1
        seq.sequence = next_val
        seq.last_generated_at = datetime.now()
        await self.db.flush()

        return next_val
