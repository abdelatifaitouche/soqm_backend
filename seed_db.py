import asyncio
from src.infra.db.seed.seed_roles import get_all_roles
from src.infra.db.seed.seed_permissions import seed_permissions
from sqlalchemy.ext.asyncio import AsyncSession
from src.infra.db.session import SessionLocal
from src.infra.db.seed.seed_role_permissions import seed_role_permissions
from src.infra.db.seed.seed_super_user import seed_super_user
from src.infra.db.seed.seed_soqm_components import seed_components
from data.soqm_data import SOQM_COMPONENTS_SEED_DATA


async def run(session: AsyncSession):
    print("Starting the script")
    print("Seeding permissions")
    await seed_permissions(session)
    print("Permissions added")
    print("Seeding roles")
    await get_all_roles(session)
    print("Seeding relationship")
    await seed_role_permissions(session)

    print("seeding super user")

    await seed_super_user(session)
    print("seeding soqm components")
    await seed_components(SOQM_COMPONENTS_SEED_DATA, session, force=False)
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
