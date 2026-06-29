from sqlalchemy.ext.asyncio import AsyncSession
from src.core.pagination import Pagination
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
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
        stmt = select(self.model).options(
            selectinload(UserDB.user_roles).selectinload(UserRolesDB.role)
        )
        stmt = self._apply_pagination(stmt, pagination)
        results = await self.db.execute(stmt)

        data = results.scalars().all()

        return [self._to_domain(u) for u in data]

    async def save(self, user: UserCreate) -> UserEntity:
        orm = self._to_orm(user)
        self.db.add(orm)
        await self.db.flush()

        await self.add_user_role(orm.id, user.role_id)

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
        print(f"from the repo getting the data : {data}")
        if not data:
            return None
        print(f"from the repoistory : {data.id}")
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

    async def add_user_role(self, user_id: UUID, role_id: UUID):
        await self.db.execute(
            pg_insert(UserRolesDB)
            .values({"user_id": user_id, "role_id": role_id})
            .on_conflict_do_nothing()
        )

    async def list_roles(self):
        from src.features.auth.models.role import Role as RoleDB

        stmt = select(RoleDB)
        results = await self.db.execute(stmt)

        data = results.scalars().all()

        return [{"id": r.id, "name": r.name} for r in data]

    async def list_options(self):
        stmt = select(self.model.id, self.model.email).where(
            self.model.is_active == True
        )

        results = (await self.db.execute(stmt)).mappings().all()

        return [{"id": res.id, "email": res.email} for res in results]
