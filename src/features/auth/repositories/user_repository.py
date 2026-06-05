from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload, contains_eager
from src.features.auth.models.user import User as UserDB
from src.features.auth.models.user_roles import UserRoles as UserRolesDB
from src.features.auth.domain.user import User as UserEntity
from uuid import UUID


class UserRepository:
    model = UserDB

    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    def _to_domain(self, orm: UserDB) -> UserEntity:
        roles = []
        if orm.user_roles:
            roles = [r.role.name for r in orm.user_roles]
        return UserEntity(
            id=orm.id,
            email=orm.email,
            password_hashed=orm.password_hash,
            last_name=orm.last_name,
            first_name=orm.first_name,
            is_active=orm.is_active,
            roles=roles,
        )

    async def get_by_id(self, user_id: UUID) -> UserEntity | None:
        stmt = (
            select(self.model)
            .where(self.model.id == user_id)
            .join(UserDB.user_roles)
            .join(UserRolesDB.role)
            .options(contains_eager(UserDB.user_roles).contains_eager(UserRolesDB.role))
        )

        result = await self.db.execute(stmt)

        data = result.unique().scalar_one_or_none()

        if not data:
            return None

        return self._to_domain(data)

    async def get_by_email(self, email: str) -> UserEntity | None:

        stmt = (
            select(self.model)
            .where(self.model.email == email)
            .join(UserDB.user_roles)
            .join(UserRolesDB.role)
            .options(contains_eager(UserDB.user_roles).contains_eager(UserRolesDB.role))
        )

        result = await self.db.execute(stmt)

        data = result.unique().scalar_one_or_none()

        if not data:
            return None

        return self._to_domain(data)
