class RiskResponseRepository:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db
