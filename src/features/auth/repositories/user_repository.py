from sqlalchemy.ext.asyncio import AsyncSession
from src.core.pagination import Pagination
from sqlalchemy import select
from sqlalchemy.orm import selectinload, contains_eager
from src.features.auth.models.user import User as UserDB
from src.features.auth.models.user_roles import UserRoles as UserRolesDB
from src.features.auth.domain.user import User as UserEntity, UserCreate
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

    def _to_orm(self, user: UserCreate) -> UserDB:
        return UserDB(
            first_name=user.first_name,
            last_name=user.last_name,
            password_hash=user.password,
            email=user.email,
        )

    def _apply_pagination(self, stmt, pagination: Pagination):
        return stmt.limit(pagination.limit).offset(pagination.offset)

    async def list(self, pagination: Pagination) -> list[UserEntity]:
        stmt = select(self.model)
        stmt = self._apply_pagination(stmt, pagination)
        results = await self.db.execute(stmt)

        data = results.scalars().all()
        return [
            UserEntity(
                id=u.id,
                first_name=u.first_name,
                last_name=u.last_name,
                email=u.email,
                is_active=u.is_active,
            )
            for u in data
        ]

    async def save(self, user: UserCreate) -> UserEntity:
        orm = self._to_orm(user)
        self.db.add(orm)
        await self.db.flush()
        await self.db.refresh(orm)
        return UserEntity(
            id=orm.id,
            email=orm.email,
            first_name=orm.first_name,
            last_name=orm.last_name,
            is_active=orm.is_active,
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

    async def get_role_permissions(self, role: str):
        return
