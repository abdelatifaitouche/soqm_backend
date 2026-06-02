import asyncio
from src.infra.db.seed.seed_roles import get_all_roles
from src.infra.db.seed.seed_permissions import seed_permissions
from sqlalchemy.ext.asyncio import AsyncSession
from src.infra.db.session import SessionLocal


async def run(session: AsyncSession):
    print("Starting the script")
    print("Seeding permissions")
    await seed_permissions(session)
    print("Permissions added")
    print("Seeding roles")
    await get_all_roles(session)
    print("finish ......")


async def main():
    print("getting db connection ......")
    async with SessionLocal() as session:
        try:
            await run(session)
            await session.commit()

        except:
            await session.rollback()
            raise
        finally:
            await session.close()


if __name__ == "__main__":
    asyncio.run(main())
