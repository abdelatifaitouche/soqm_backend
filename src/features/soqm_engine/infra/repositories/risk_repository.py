from uuid import UUID
from src.features.soqm_engine.domain.entities.risk import Risk
from sqlalchemy.ext.asyncio import AsyncSession
from src.features.soqm_engine.application.ports import IRiskRepository


class RiskRepository(IRiskRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, risk: Risk) -> None:
        pass

    async def get(self, risk_id: UUID) -> Risk | None:
        pass

    async def delete(self, risk_id: UUID) -> None:
        pass
