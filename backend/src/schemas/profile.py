"""Pydantic schemas for profile endpoints."""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ProfileResponse(BaseModel):
    """User profile response."""

    id: str
    username: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    bio: Optional[str]
    avatar_url: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class ProfileUpdate(BaseModel):
    """Update profile request."""

    first_name: Optional[str] = Field(None, max_length=255)
    last_name: Optional[str] = Field(None, max_length=255)
    bio: Optional[str] = None
    avatar_url: Optional[str] = Field(None, max_length=500)


class ChangePasswordRequest(BaseModel):
    """Change password request."""

    current_password: str
    new_password: str = Field(..., min_length=8)
    confirm_password: str


class PreferenceResponse(BaseModel):
    """User preferences response."""

    id: str
    user_id: str
    theme: str
    llm_model: str
    llm_temperature: float
    llm_max_tokens: int
    ide_type: Optional[str]
    auto_sync: bool
    notifications_enabled: bool

    class Config:
        from_attributes = True


class PreferenceUpdate(BaseModel):
    """Update preferences request."""

    theme: Optional[str] = Field(None, pattern="^(light|dark)$")
    llm_model: Optional[str] = None
    llm_temperature: Optional[float] = Field(None, ge=0.0, le=1.0)
    llm_max_tokens: Optional[int] = Field(None, gt=0)
    ide_type: Optional[str] = None
    auto_sync: Optional[bool] = None
    notifications_enabled: Optional[bool] = None
