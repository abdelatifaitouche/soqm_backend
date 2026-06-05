from fastapi.security import HTTPBearer
from fastapi.requests import Request
from fastapi.exceptions import HTTPException
from fastapi import status, Depends
from src.features.auth.security.jwt import decode_access_token
from src.core.exceptions import WrongCredentialsError


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
    return payload
