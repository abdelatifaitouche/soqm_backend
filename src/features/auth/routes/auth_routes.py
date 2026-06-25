from fastapi import APIRouter, Depends, Response, status
from uuid import UUID
from src.core.pagination import Pagination
from sqlalchemy.ext.asyncio import AsyncSession
from src.features.auth.schemas.user import (
    UserLogin,
    CreateUser,
    UserRead,
    AssignRoleRequest,
)
from src.features.auth.schemas.role import Role as RoleRead
from src.features.auth.domain.user import User
from src.infra.db.uow import get_db
from src.features.auth.services.auth_service import AuthService
from src.features.auth.repositories.user_repository import UserRepository
from src.features.auth.mappers.user_mapper import UserMapper
from src.features.auth.security.dependencies import require_auth
from fastapi.requests import Request
from src.features.auth.security.jwt import decode_refresh_token, generate_access_token
from src.core.exceptions import (
    UserNotFoundError,
    TokenExpiredError,
    TokenInvalidError,
    RefreshTokenMissingError,
    AccessDenied,
)
from src.features.auth.security.dependencies import require_permissions
from src.features.auth.permissions.auth_permissions import AuthPermissions
from src.core.config import settings

router = APIRouter(prefix="/auth")


def get_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    repo: UserRepository = UserRepository(db)
    return AuthService(repo)


@router.post("/login/")
async def login(
    data: UserLogin,
    response: Response,
    service: AuthService = Depends(get_service),
):
    access, refresh = await service.login_user(UserMapper.from_login(data))

    response.set_cookie(
        key="refresh_token",
        value=refresh,
        path="/",
        secure=False if settings.DEBUG else True,
        httponly=True,
        samesite="lax",
    )

    return {"access_token": access}


@router.post("/logout/")
async def logout():
    raise NotImplementedError()


@router.post("/refresh/")
async def get_refresh(
    request: Request,
    response: Response,
    service: AuthService = Depends(get_service),
):
    ref: str | None = request.cookies.get("refresh_token")

    try:
        access, refresh = await service.generate_tokens(ref)
    except (
        TokenInvalidError,
        TokenExpiredError,
        UserNotFoundError,
        RefreshTokenMissingError,
    ):
        response.delete_cookie("refresh_token")
        raise

    response.set_cookie(
        key="refresh_token",
        value=refresh,
        path="/",
        secure=False,
        httponly=True,
        samesite="lax",
    )

    return {"access_token": access}


@router.post("/register/")
async def create_user(
    data: CreateUser,
    creds=Depends(require_permissions(AuthPermissions.CREATE)),
    service: AuthService = Depends(get_service),
):
    user: User = await service.create_user(UserMapper.from_create(data))
    return UserRead.model_validate(user)


@router.get("/list")
async def list_users(
    pagination: Pagination = Depends(),
    creds=Depends(require_permissions(AuthPermissions.READ)),
    service: AuthService = Depends(get_service),
):
    users: list[User] = await service.list(pagination)
    return [UserRead.model_validate(u) for u in users]


@router.patch("/{user_id}/block/")
async def deactivate_user(
    user_id: str,
    service: AuthService = Depends(get_service),
    creds=Depends(
        require_permissions(AuthPermissions.BLOCK),
    ),
):

    return


@router.get("/roles")
async def list_roles(
    service: AuthService = Depends(get_service),
):
    roles = await service.list_roles()
    return [RoleRead.model_validate(r) for r in roles]


@router.post("/{user_id}/roles/", status_code=status.HTTP_204_NO_CONTENT)
async def assing_role(
    user_id: str,
    payload: AssignRoleRequest,
    service: AuthService = Depends(get_service),
):
    return await service.assign_role(UUID(user_id), payload.role_id)
