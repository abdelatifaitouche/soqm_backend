
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.features.findings.infra.models import (
    RootCauseCategory,
    RootCauseIndicator,
)


class RcaTrackerQueryService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(self):

        stmt = select(RootCauseCategory).options(
            selectinload(RootCauseCategory.root_cause_indicators).selectinload(
                RootCauseIndicator.potential_root_causes
            )
        )

        res = (await self.session.execute(stmt)).mappings().all()

        return res
