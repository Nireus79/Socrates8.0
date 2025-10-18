"""Pydantic schemas for authentication endpoints."""

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """User registration request."""

    username: str = Field(..., min_length=3, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=8)
    first_name: str = Field(None, max_length=255)
    last_name: str = Field(None, max_length=255)


class LoginRequest(BaseModel):
    """User login request."""

    username: str
    password: str


class RefreshTokenRequest(BaseModel):
    """Token refresh request."""

    refresh_token: str


class TokenResponse(BaseModel):
    """Token response."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int


class LoginResponse(BaseModel):
    """Login response with user data."""

    user_id: str
    username: str
    email: str
    first_name: str | None
    last_name: str | None
    access_token: str
    token_type: str = "bearer"
    expires_in: int
