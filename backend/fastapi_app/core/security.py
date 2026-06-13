from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
from jose import JWTError, jwt

from .config import settings


class JWTHandler:
    """Handles JWT creation and verification for access and refresh tokens."""

    @staticmethod
    def create_access_token(
        subject: str | int, extra_claims: dict[str, Any] | None = None
    ) -> str:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
        payload: dict[str, Any] = {
            "sub": str(subject),
            "exp": expire,
            "type": "access",
        }
        if extra_claims:
            payload.update(extra_claims)
        return jwt.encode(
            payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )

    @staticmethod
    def create_refresh_token(subject: str | int) -> str:
        expire = datetime.now(timezone.utc) + timedelta(
            days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
        )
        payload: dict[str, Any] = {
            "sub": str(subject),
            "exp": expire,
            "type": "refresh",
        }
        return jwt.encode(
            payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )

    @staticmethod
    def decode_token(token: str) -> dict[str, Any]:
        try:
            payload = jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
            return payload
        except JWTError as exc:
            raise ValueError("Invalid or expired token") from exc

    @staticmethod
    def get_subject(token: str) -> str:
        payload = JWTHandler.decode_token(token)
        subject: str | None = payload.get("sub")
        if subject is None:
            raise ValueError("Token missing subject claim")
        return subject


class PasswordHandler:
    """Handles password hashing and verification using bcrypt directly."""

    @staticmethod
    def hash(plain_password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(plain_password.encode("utf-8"), salt).decode("utf-8")

    @staticmethod
    def verify(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )
