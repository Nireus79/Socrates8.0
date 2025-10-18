"""JWT token handling for authentication."""

from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from uuid import UUID

from backend.src.config import settings


class JWTHandler:
    """Handler for JWT token operations."""

    @staticmethod
    def create_access_token(
        user_id: UUID,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create access token.

        Args:
            user_id: User ID to encode
            expires_delta: Optional expiration delta

        Returns:
            JWT token string
        """
        to_encode = {"sub": str(user_id)}

        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=settings.JWT_EXPIRE_MINUTES
            )

        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(
            to_encode,
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM
        )

        return encoded_jwt

    @staticmethod
    def create_refresh_token(user_id: UUID) -> str:
        """Create refresh token with longer expiration.

        Args:
            user_id: User ID to encode

        Returns:
            JWT refresh token string
        """
        # Refresh token valid for 7 days
        expires_delta = timedelta(days=7)
        return JWTHandler.create_access_token(user_id, expires_delta)

    @staticmethod
    def verify_token(token: str) -> Optional[str]:
        """Verify token and extract user ID.

        Args:
            token: JWT token

        Returns:
            User ID string or None if invalid

        Raises:
            JWTError: If token is invalid
        """
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=[settings.JWT_ALGORITHM]
            )
            user_id: str = payload.get("sub")

            if user_id is None:
                return None

            return user_id

        except JWTError:
            return None

    @staticmethod
    def decode_token(token: str) -> Optional[dict]:
        """Decode token and return payload.

        Args:
            token: JWT token

        Returns:
            Payload dict or None if invalid
        """
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=[settings.JWT_ALGORITHM]
            )
            return payload

        except JWTError:
            return None

    @staticmethod
    def is_token_expired(token: str) -> bool:
        """Check if token is expired.

        Args:
            token: JWT token

        Returns:
            True if expired
        """
        payload = JWTHandler.decode_token(token)

        if not payload:
            return True

        exp = payload.get("exp")

        if not exp:
            return True

        return datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(timezone.utc)
