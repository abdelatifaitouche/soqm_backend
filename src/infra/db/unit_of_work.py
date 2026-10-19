from sqlalchemy.ext.asyncio import AsyncSession

from src.core.shared.interfaces.unit_of_work import IUnitOfWork


class UnitOfWork(IUnitOfWork):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def __aenter__(self):
        if not self._session.in_transaction:
            await self._session.begin()
        return self

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
