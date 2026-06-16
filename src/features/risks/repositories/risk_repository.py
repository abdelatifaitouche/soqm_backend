from sqlalchemy.ext.asyncio import AsyncSession


class RiskRepository:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db
