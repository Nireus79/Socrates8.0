"""Pydantic schemas for session endpoints."""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from uuid import UUID


class SessionCreate(BaseModel):
    """Create session request."""

    project_id: Optional[UUID] = None
    name: Optional[str] = None
    mode: str = Field("chat", pattern="^(chat|question|teaching|review)$")
    role: Optional[str] = None


class SessionUpdate(BaseModel):
    """Update session request."""

    name: Optional[str] = None
    mode: Optional[str] = Field(None, pattern="^(chat|question|teaching|review)$")
    status: Optional[str] = None


class SessionToggleMode(BaseModel):
    """Toggle session mode request."""

    mode: str = Field(..., pattern="^(chat|question|teaching|review)$")


class SessionResponse(BaseModel):
    """Session response."""

    id: str
    name: Optional[str]
    status: str
    mode: str
    role: Optional[str]
    project_id: Optional[str]
    owner_id: str
    created_at: datetime
    updated_at: datetime
    message_count: int = 0

    class Config:
        from_attributes = True


class SessionListResponse(BaseModel):
    """List of sessions response."""

    sessions: List[SessionResponse]
    total: int
    page: int
    limit: int
