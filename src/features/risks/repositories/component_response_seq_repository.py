from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from src.features.risks.models.component_response_seq import ComponentResponseSeq
from datetime import datetime


class ComponentResponseSeqRepository:
    model = ComponentResponseSeq

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_next_val(self, component_id: UUID):
        stmt = select(self.model).where(self.model.component_id == component_id)

        seq: ComponentResponseSeq | None = (
            await self.db.execute(stmt)
        ).scalar_one_or_none()

        if seq is None:
            seq = ComponentResponseSeq(
                component_id=component_id,
                sequence=0,
            )
            self.db.add(seq)
            await self.db.flush()

        next_val: int = seq.sequence + 1
        seq.sequence = next_val
        seq.last_generated_at = datetime.now()
        await self.db.flush()
        return next_val
