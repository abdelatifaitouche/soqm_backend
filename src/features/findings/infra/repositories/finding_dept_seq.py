from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from uuid import UUID
from src.features.findings.infra.models import FindingDeptSeq
from src.features.findings.application.ports.ifinding_dept_seq_repo import (
    IFindingDeptSeqRepository,
)


class FindingDeptSequenceRepository(IFindingDeptSeqRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def inc_get(self, department_id: UUID) -> int:
        insert_stmt = insert(FindingDeptSeq).values(
            {
                "department_id": department_id,
                "seq": 1,
            }
        )

        upsert_stmt = insert_stmt.on_conflict_do_update(
            index_elements=["department_id"],
            set_={
                "seq": FindingDeptSeq.seq + 1,
            },
        ).returning(FindingDeptSeq.seq)

        next_val = (await self.session.execute(upsert_stmt)).scalar_one()

        return next_val
