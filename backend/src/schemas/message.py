"""Pydantic schemas for message endpoints."""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class MessageCreate(BaseModel):
    """Create message request."""

    content: str = Field(..., min_length=1, max_length=10000)
    message_type: str = Field("text", pattern="^(text|code|question)$")


class MessageResponse(BaseModel):
    """Message response."""

    id: str
    session_id: str
    user_id: str
    role: str
    content: str
    message_type: str
    created_at: datetime

    class Config:
        from_attributes = True


class MessageListResponse(BaseModel):
    """List of messages response."""

    messages: List[MessageResponse]
    total: int
    page: int
    limit: int


class SendMessageResponse(BaseModel):
    """Response when sending a message."""

    user_message: MessageResponse
    assistant_response: MessageResponse
