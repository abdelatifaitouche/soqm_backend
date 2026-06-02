from src.core.roles import Role as RoleEnums
from src.features.auth.models.role import Role
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession


async def get_all_roles(session: AsyncSession):
    all_roles = [{"name": r.value, "is_system": True} for r in RoleEnums]

    result = await session.execute(
        insert(Role).values(all_roles).on_conflict_do_nothing(),
    )

    return result
