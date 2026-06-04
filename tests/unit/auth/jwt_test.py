import pytest
import uuid

from src.features.auth.security.jwt import (
    generate_access_token,
    generate_refresh_token,
    decode_access_token,
    decode_refresh_token,
)
from datetime import datetime, timezone


@pytest.fixture
def user():
    return {
        "user_id": str(uuid.uuid4()),
        "role": "SUPER_ADMIN",
        "email": "super@gmail.com",
    }


class TestJwtToken:
    def test_access_token_generation(self, user):
        token = generate_access_token(
            user["user_id"],
            user["email"],
            user["role"],
        )
        assert isinstance(token, str) == True
        assert len(token) > 0

    def test_refresh_token_generation(self, user):
        token = generate_refresh_token(user["user_id"])

        assert isinstance(token, str) == True
        assert len(token) > 0

    def test_access_not_refresh(self, user):
        access_token = generate_access_token(
            user["user_id"], user["email"], user["role"]
        )
        refresh_token = generate_refresh_token(user["user_id"])

        assert isinstance(access_token, str) == True
        assert isinstance(refresh_token, str) == True

        assert len(access_token) > 0
        assert len(refresh_token) > 0

        assert access_token != refresh_token

    def test_decode_access_token(self, user):
        access_token = generate_access_token(
            user["user_id"], user["email"], user["role"]
        )

        decoded_access = decode_access_token(access_token)

        assert decoded_access is not None
        assert isinstance(decoded_access, dict) == True

        assert decoded_access.get("type") == "ACCESS_TOKEN"
        assert decoded_access.get("sub") == user["user_id"]
        assert decoded_access.get("email") == user["email"]
        assert decoded_access.get("role") == user["role"]
