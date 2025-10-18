"""Tests for authentication module."""

import pytest
from datetime import timedelta
from uuid import uuid4

from backend.src.auth.jwt_handler import JWTHandler
from backend.src.config import settings


class TestJWTHandler:
    """Tests for JWT token handling."""

    def test_create_access_token(self):
        """Test creating access token."""
        user_id = uuid4()
        token = JWTHandler.create_access_token(user_id)

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_access_token_with_expiration(self):
        """Test creating token with custom expiration."""
        user_id = uuid4()
        expires_delta = timedelta(hours=1)
        token = JWTHandler.create_access_token(user_id, expires_delta)

        assert token is not None
        assert isinstance(token, str)

    def test_create_refresh_token(self):
        """Test creating refresh token."""
        user_id = uuid4()
        token = JWTHandler.create_refresh_token(user_id)

        assert token is not None
        assert isinstance(token, str)

    def test_verify_token_valid(self):
        """Test verifying valid token."""
        user_id = uuid4()
        token = JWTHandler.create_access_token(user_id)

        extracted_user_id = JWTHandler.verify_token(token)

        assert extracted_user_id is not None
        assert extracted_user_id == str(user_id)

    def test_verify_token_invalid(self):
        """Test verifying invalid token."""
        invalid_token = "invalid.token.here"

        result = JWTHandler.verify_token(invalid_token)

        assert result is None

    def test_verify_token_malformed(self):
        """Test verifying malformed token."""
        malformed_token = "not-a-valid-jwt"

        result = JWTHandler.verify_token(malformed_token)

        assert result is None

    def test_decode_token_valid(self):
        """Test decoding valid token."""
        user_id = uuid4()
        token = JWTHandler.create_access_token(user_id)

        payload = JWTHandler.decode_token(token)

        assert payload is not None
        assert payload.get("sub") == str(user_id)
        assert "exp" in payload

    def test_decode_token_invalid(self):
        """Test decoding invalid token."""
        invalid_token = "invalid.token.here"

        result = JWTHandler.decode_token(invalid_token)

        assert result is None

    def test_is_token_expired_valid(self):
        """Test checking expiration on valid token."""
        user_id = uuid4()
        token = JWTHandler.create_access_token(user_id)

        is_expired = JWTHandler.is_token_expired(token)

        assert is_expired is False

    def test_is_token_expired_invalid(self):
        """Test checking expiration on invalid token."""
        invalid_token = "invalid.token.here"

        is_expired = JWTHandler.is_token_expired(invalid_token)

        assert is_expired is True

    def test_token_contains_user_id(self):
        """Test that token contains user ID."""
        user_id = uuid4()
        token = JWTHandler.create_access_token(user_id)

        # Verify we can extract the user ID
        extracted_id = JWTHandler.verify_token(token)

        assert extracted_id == str(user_id)

    def test_different_tokens_different_users(self):
        """Test that different users get different tokens."""
        user_id_1 = uuid4()
        user_id_2 = uuid4()

        token_1 = JWTHandler.create_access_token(user_id_1)
        token_2 = JWTHandler.create_access_token(user_id_2)

        assert token_1 != token_2

        extracted_id_1 = JWTHandler.verify_token(token_1)
        extracted_id_2 = JWTHandler.verify_token(token_2)

        assert extracted_id_1 != extracted_id_2
        assert extracted_id_1 == str(user_id_1)
        assert extracted_id_2 == str(user_id_2)

    def test_token_settings_used(self):
        """Test that token uses settings correctly."""
        user_id = uuid4()
        token = JWTHandler.create_access_token(user_id)

        payload = JWTHandler.decode_token(token)

        assert payload is not None
        assert "exp" in payload
        assert "sub" in payload

    def test_create_multiple_tokens_same_user(self):
        """Test creating multiple tokens for same user."""
        import time
        user_id = uuid4()

        token_1 = JWTHandler.create_access_token(user_id)
        time.sleep(0.1)  # Sleep to ensure different expiration times
        token_2 = JWTHandler.create_access_token(user_id)

        # Both should verify to same user
        assert JWTHandler.verify_token(token_1) == str(user_id)
        assert JWTHandler.verify_token(token_2) == str(user_id)

    def test_refresh_token_longer_expiry(self):
        """Test that refresh token has longer expiry."""
        user_id = uuid4()

        access_token = JWTHandler.create_access_token(user_id)
        refresh_token = JWTHandler.create_refresh_token(user_id)

        access_payload = JWTHandler.decode_token(access_token)
        refresh_payload = JWTHandler.decode_token(refresh_token)

        access_exp = access_payload.get("exp")
        refresh_exp = refresh_payload.get("exp")

        # Refresh token should expire later
        assert refresh_exp > access_exp

    def test_token_payload_structure(self):
        """Test token payload structure."""
        user_id = uuid4()
        token = JWTHandler.create_access_token(user_id)

        payload = JWTHandler.decode_token(token)

        assert payload is not None
        assert "sub" in payload
        assert "exp" in payload
        assert payload["sub"] == str(user_id)

    def test_verify_token_returns_string(self):
        """Test that verify_token returns string user_id."""
        user_id = uuid4()
        token = JWTHandler.create_access_token(user_id)

        result = JWTHandler.verify_token(token)

        assert isinstance(result, str)
        assert result == str(user_id)
