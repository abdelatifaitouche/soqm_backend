from sqlalchemy.ext.asyncio import AsyncSession
from src.features.auth.models.role import Role as RoleDB
from src.features.auth.models.permission import Permission
from src.features.auth.models.role_permissions import RolePermissions
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from src.core.roles import Role
from src.features.auth.permissions.auth_permissions import AuthPermissions
from src.features.soqm_components.permissions.components_permissions import (
    ComponentPermissions,
)


ROLES_PERMISSIONS = {
    Role.SUPER_ADMIN: [
        AuthPermissions.CREATE,
        AuthPermissions.ACTIVATE,
        AuthPermissions.BLOCK,
        AuthPermissions.DELETE,
        AuthPermissions.READ,
        AuthPermissions.READ_OWN,
        AuthPermissions.UPDATE,
        ComponentPermissions.ACTIVATE,
        ComponentPermissions.CREATE,
        ComponentPermissions.DEACTIVATE,
        ComponentPermissions.DELETE,
        ComponentPermissions.READ,
        ComponentPermissions.UPDATE,
    ],
    Role.ADMIN: [
        AuthPermissions.CREATE,
        AuthPermissions.ACTIVATE,
        AuthPermissions.BLOCK,
        AuthPermissions.DELETE,
        AuthPermissions.READ,
        AuthPermissions.READ_OWN,
        AuthPermissions.UPDATE,
        ComponentPermissions.ACTIVATE,
        ComponentPermissions.CREATE,
        ComponentPermissions.DEACTIVATE,
        ComponentPermissions.DELETE,
        ComponentPermissions.READ,
        ComponentPermissions.UPDATE,
    ],
    Role.MANAGER: [
        AuthPermissions.READ,
        AuthPermissions.READ_OWN,
        ComponentPermissions.READ,
    ],
    Role.OPERATOR: [
        AuthPermissions.READ_OWN,
        ComponentPermissions.READ,
    ],
}


async def fetch_data(session: AsyncSession, model):

    stmt = select(model)

    result = await session.execute(stmt)

    return result.scalars().all()


async def seed_role_permissions(session: AsyncSession):

    all_roles = await fetch_data(session, RoleDB)

    if not all_roles:
        raise Exception("Please, run seed roles first")

    roles_map = {r.name: r.id for r in all_roles}

    all_permissions = await fetch_data(session, Permission)

    if not all_permissions:
        raise Exception("Please, run seed permissions first")

    perms_map = {
        (
            p.resource,
            p.action,
        ): p.id
        for p in all_permissions
    }

    data_to_insert = []
    for role, permissions in ROLES_PERMISSIONS.items():
        if not permissions:
            continue

        r_id = roles_map[role.value]

        for p in permissions:
            data_to_insert.append({"role_id": r_id, "permission_id": perms_map[p]})

    result = await session.execute(
        pg_insert(RolePermissions).values(data_to_insert).on_conflict_do_nothing()
    )

    print("Script ended, all inserted .........")
