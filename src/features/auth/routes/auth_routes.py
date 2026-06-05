from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from src.features.auth.schemas.user import UserLogin
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
)

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
        secure=False,
        httponly=True,
        samesite="lax",
    )

    return {"access_token": access}


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
    creds=Depends(require_auth),
    service: AuthService = Depends(get_service),
):
    return creds
