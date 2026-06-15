from src.infra.db.session import SessionLocal

"""
    This contains a bug to fix in the next deployment,

    BUG:
        endpoint returns before the session commited and closed,
        client may recv 2XX, but in the same time the server hits an issue,
        session.rolledback,
        now Invalid state

        to fix this, 
            several designs may arise, but each one has downsides,
            of the fixes, is to place the commit/rollback logic in the service/usecase
            but this will introduce the dependcey of the service with the database,
            
            fix : 
                Unit of Work pattern that gets plugged in the service, and handle the 
                commit/rollback directly
                    a context manager : 
                    with uow() as uow:
                        work()
                    class UnitOfWork:
                        def __aenter__()
                        def __aexit__()
                        def commit()
                        def rollback()

                    class service:
                        def __ini__(uow)
                            self.uow = uow (contains the session and the repo maye be)
"""


async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()

        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
