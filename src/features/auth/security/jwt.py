import jwt
from src.core.config import settings
import uuid
from datetime import datetime, timedelta, timezone
from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidAlgorithmError,
    InvalidTokenError,
)
from src.features.auth.enums.tokens import TokenType
from src.core.exceptions import TokenExpiredError, TokenInvalidError


def _now() -> datetime:
    return datetime.now(timezone.utc)


_TOKEN_CONFIG = {
    TokenType.ACCESS_TOKEN: {
        "expires": timedelta(hours=settings.ACCESS_TOKEN_TIME),
    },
    TokenType.REFRESH_TOKEN: {
        "expires": timedelta(days=settings.REFRESH_TOKEN_TIME),
    },
}


def _build_base_claims(token_type: TokenType):
    iat: datetime = _now()

    return {
        "jti": str(uuid.uuid4()),
        "iat": iat,
        "exp": iat + _TOKEN_CONFIG[token_type]["expires"],
        "type": token_type.value,
    }


def _encode(payload) -> str:
    return jwt.encode(
        payload,
        key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGO,
    )


# PUBLIC API
def generate_refresh_token(user_id: uuid.UUID) -> str:

    iat: datetime = _now()

    payload = {"sub": str(user_id), **_build_base_claims(TokenType.REFRESH_TOKEN)}

    return _encode(payload)


def generate_access_token(user_id: uuid.UUID, email: str, role: str) -> str:
    iat: datetime = _now()

    payload = {
        "sub": str(user_id),
        "email": email,
        "role": role,
        **_build_base_claims(TokenType.ACCESS_TOKEN),
    }

    return _encode(payload)


def _decode(token: str, token_type: TokenType):
    try:
        decoded = jwt.decode(
            token,
            key=settings.JWT_SECRET_KEY,
            algorithms=[
                settings.JWT_ALGO,
            ],
        )
    except ExpiredSignatureError as exp:
        raise TokenExpiredError(message="Token Expired")
    except InvalidTokenError as inv:
        raise TokenInvalidError(message="Invalid Token")

    if decoded.get("type") != token_type.value:
        raise TokenInvalidError(message="Invalid Token")
    return decoded


# PUBLIC API
def decode_access_token(token: str):
    return _decode(token, TokenType.ACCESS_TOKEN)


def decode_refresh_token(token: str):
    return _decode(token, TokenType.REFRESH_TOKEN)
