from src.features.auth.schemas.user import UserLogin, CreateUser
from src.features.auth.domain.user import (
    UserLogin as UserLoginEntity,
    UserCreate as UserCreateEntity,
)


class UserMapper:
    @staticmethod
    def from_login(data: UserLogin) -> UserLoginEntity:
        return UserLoginEntity(
            email=data.email,
            password=data.password,
        )

    @staticmethod
    def from_create(data: CreateUser) -> UserCreateEntity:
        return UserCreateEntity(
            first_name=data.first_name,
            last_name=data.last_name,
            password=data.password,
            email=data.email,
            role_id=data.role_id,
        )
