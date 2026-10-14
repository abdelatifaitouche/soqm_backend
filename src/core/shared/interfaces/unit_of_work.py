from abc import ABC, abstractmethod


class IUnitOfWork(ABC):
    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exc_type,
        exc_val,
        exc_tb,
    ):

        try:
            if exc_type is not None:
                await self.rollback()
            else:
                await self.commit()
        except Exception as e:
            await self.rollback()
            raise e

    @abstractmethod
    async def commit(self):
        raise NotImplementedError()

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError()
