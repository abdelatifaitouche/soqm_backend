from src.features.auth.schemas.user import UserLogin
from src.features.auth.domain.user import UserLogin as UserLoginEntity


class UserMapper:
    @staticmethod
    def from_login(data: UserLogin) -> UserLoginEntity:
        return UserLoginEntity(
            email=data.email,
            password=data.password,
        )
