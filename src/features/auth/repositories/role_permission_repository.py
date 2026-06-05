from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.features.auth.models.permission import Permission
from src.features.auth.models.role import Role
from src.features.auth.models.role_permissions import RolePermissions
from src.features.auth.domain.permission import Permission as PermissionEntity


class RolePermissionRepository:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    def _to_domain(self, orm: Permission) -> PermissionEntity:
        return PermissionEntity(
            resource=orm.resource,
            action=orm.action,
        )

    async def get_role_permissions(self, role: str):

        stmt = (
            select(Permission).join(RolePermissions).join(Role).where(Role.name == role)
        )

        result = await self.db.execute(stmt)

        permissions = result.scalars().all()
        return {
            (
                row.resource,
                row.action,
            )
            for row in permissions
        }
