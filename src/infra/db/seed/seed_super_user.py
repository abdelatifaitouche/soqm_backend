# first grab all the roles_id
# create the user  {first_name,last_name, email , password(hashed) , is_active=True,}
# get the user_roles associoation , associtate this user_id with the super_admin_role_id
# commit everything

from sqlalchemy.ext.asyncio import AsyncSession
from src.features.risks.models.risk import Risk
from src.features.auth.models.role import Role as RoleDB
from src.features.auth.models.user import User as UserDB
from src.features.auth.models.user_roles import UserRoles as UserRolesDB
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy import select, text
from src.core.roles import Role as ROLE_ENUM
from src.core.config import settings
from src.features.auth.security.password import hash_password
import uuid
from uuid import UUID


async def check_super_user(session: AsyncSession):
    query = text(
        """ SELECT u.id, r.name FROM user_roles ur JOIN users u ON ur.user_id=u.id JOIN roles r ON ur.role_id=r.id WHERE r.name='SUPER_ADMIN' """
    )
    result = await session.execute(query)

    data = result.scalar_one_or_none()
    if not data:
        return False
    return True


async def fetch_super_admin_role(session: AsyncSession) -> RoleDB:
    print("Fetching the super admin role from DB ..............")
    result = await session.execute(
        select(RoleDB).where(RoleDB.name == ROLE_ENUM.SUPER_ADMIN)
    )

    data = result.scalar_one_or_none()

    if not data:
        raise Exception("Please, run the seed roles first")
    print("Super admin Role fetched ............ OK")
    return data


def build_super_user():
    print("Building the Super User ........\nPassword Hashing ........")
    hashed_password: str = hash_password(settings.SUPER_USER_PWD)
    return {
        "id": uuid.uuid4(),
        "first_name": settings.SUPER_USER_NAME,
        "last_name": settings.SUPER_USER_LAST,
        "password_hash": hashed_password,
        "email": settings.SUPER_USER_EMAIL,
        "is_active": True,
    }


def associating_user_role(user_id: UUID, role_id: UUID):
    return {"user_id": user_id, "role_id": role_id}


async def seed_super_user(session: AsyncSession):

    if await check_super_user(session):
        return

    sp_user = build_super_user()
    print("Inserting super user in db ..........")
    result = await session.execute(
        pg_insert(UserDB)
        .values(
            sp_user,
        )
        .on_conflict_do_nothing()
        .returning(UserDB)
    )

    user = result.scalar_one_or_none()

    print("Super User Inserted ................. OK")
    sp_role: RoleDB = await fetch_super_admin_role(session)

    user_role = associating_user_role(user.id, sp_role.id)
    print("Saving the association ..................")
    result = await session.execute(
        pg_insert(UserRolesDB)
        .values(
            user_role,
        )
        .on_conflict_do_nothing()
        .returning(UserRolesDB)
    )

    ur_r = result.scalar_one_or_none()

    if not ur_r:
        raise Exception("User Role was not joined ....... FAILED")

    print("Saved .............. OK")
