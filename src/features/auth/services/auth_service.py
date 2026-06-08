from src.features.auth.domain.user import UserLogin, User
from src.features.auth.security.password import check_password
from src.features.auth.security.jwt import (
    generate_access_token,
    generate_refresh_token,
    decode_refresh_token,
)
from src.features.auth.repositories.user_repository import UserRepository
from src.core.exceptions import (
    WrongCredentialsError,
    TokenExpiredError,
    TokenInvalidError,
    RefreshTokenMissingError,
    UserNotFoundError,
)
from uuid import UUID


class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo: UserRepository = repo

    async def create_user(self):
        return

    async def get_by_id(self, user_id: UUID):

        return await self.repo.get_by_id(user_id)

    async def login_user(self, data: UserLogin):

        user: User | None = await self.repo.get_by_email(data.email)

        if not user:
            raise WrongCredentialsError("Invalid Credentials")

        if not check_password(data.password, user.password_hashed):
            raise WrongCredentialsError("Invalid Credentials")

        if not user.is_active:
            raise WrongCredentialsError("Invalid Credentials")

        access_token: str = generate_access_token(user.id, user.email, user.roles[0])

        refresh_token: str = generate_refresh_token(user.id)

        return access_token, refresh_token

    async def generate_tokens(self, refresh_token: str | None):
        if not refresh_token:
            raise RefreshTokenMissingError(
                "Missing Refresh Token",
            )

        try:
            payload = decode_refresh_token(refresh_token)
        except TokenExpiredError:
            raise TokenExpiredError("Invalid Refresh Token")
        except TokenInvalidError:
            raise TokenInvalidError("Invalid Refresh Token")

        user: User | None = await self.repo.get_by_id(payload["sub"])

        if not user:
            raise UserNotFoundError("Invalid credentials")

        access_token: str = generate_access_token(user.id, user.email, user.roles[0])

        new_refresh_token: str = generate_refresh_token(user.id)

        return access_token, new_refresh_token

    async def update(self):
        return

    async def block_user(self):
        return

    async def activate_user(self):
        return

    async def delete(self):
        return
