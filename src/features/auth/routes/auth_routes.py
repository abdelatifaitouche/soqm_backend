from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.features.auth.schemas.user import UserLogin
from src.infra.db.uow import get_db
from src.features.auth.services.auth_service import AuthService
from src.features.auth.repositories.user_repository import UserRepository
from src.features.auth.mappers.user_mapper import UserMapper

router = APIRouter(prefix="/auth")


def get_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    repo: UserRepository = UserRepository(db)
    return AuthService(repo)


@router.post("/login/")
async def login(
    data: UserLogin,
    service: AuthService = Depends(get_service),
):
    refresh, access = await service.login_user(UserMapper.from_login(data))
    return {"refresh": refresh, "access": access}
