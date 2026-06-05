from fastapi.security import HTTPBearer
from fastapi.requests import Request
from fastapi.exceptions import HTTPException
from fastapi import status, Depends
from src.features.auth.security.jwt import decode_access_token
from src.core.exceptions import WrongCredentialsError, AccessDenied
from src.features.auth.repositories.role_permission_repository import (
    RolePermissionRepository,
)
from src.infra.db.uow import get_db


class JwtAuth(HTTPBearer):
    async def __call__(self, request: Request):
        creds = await super().__call__(request)
        if not creds:
            if self.auto_error:
                raise WrongCredentialsError(
                    message="Not Authenticated",
                )
            return None
        token: str = creds.credentials
        payload = decode_access_token(token)
        return payload


def require_auth(payload=Depends(JwtAuth())):
    """BASE function for authenticated routes"""
    return payload


def require_permissions(*permissions):
    async def check(
        payload=Depends(require_auth),
        db=Depends(get_db),
    ):
        repo = RolePermissionRepository(db)

        perms = await repo.get_role_permissions(payload["role"])

        missing = set(permissions) - set(perms)

        if missing:
            raise AccessDenied("Access Denied")

    return check
