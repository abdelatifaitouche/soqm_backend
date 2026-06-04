from src.features.auth.domain.user import UserLogin, User
from src.features.auth.security.password import check_password
from src.features.auth.security.jwt import generate_access_token, generate_refresh_token
from src.features.auth.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo: UserRepository = repo

    async def create_user(self):
        return

    async def get_by_id(self):
        return

    async def login_user(self, data: UserLogin):
        """
        Always check if the user is active before login
        """

        # first grab the user by its email

        user: User | None = await self.repo.get_by_email(data.email)

        if not user:
            raise Exception("wrong auth")

        # second check the password

        if not check_password(data.password, user.password_hashed):
            raise Exception("wrong creds")

        # check if the user is active

        if not user.is_active:
            raise Exception("roh t9owed")

        # build the tokens

        access_token: str = generate_access_token(user.id, user.email, user.roles[0])

        refresh_token: str = generate_refresh_token(user.id)
        # return them

        return access_token, refresh_token

    async def update(self):
        return

    async def block_user(self):
        return

    async def activate_user(self):
        return

    async def delete(self):
        return
