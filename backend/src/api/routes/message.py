"""Message API routes."""

from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
from uuid import UUID

from src.database import get_db
from src.services.message_service import MessageService
from src.services.session_service import SessionService
from src.dependencies import get_current_user
from src.schemas.message import MessageCreate, MessageResponse, MessageListResponse, SendMessageResponse
from src.models.user import User

router = APIRouter(tags=["messages"])


@router.get("/sessions/{session_id}/messages", response_model=MessageListResponse)
async def get_messages(
    session_id: UUID,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=500),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get message history for a session with pagination."""
    try:
        # Verify session ownership
        session_service = SessionService(db)
        session = session_service.get_session_by_id(session_id)

        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        if session.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to view this session")

        # Get messages
        message_service = MessageService(db)
        total = message_service.count_messages(session_id=session_id)

        messages = message_service.get_messages_paginated(
            session_id=session_id,
            page=page,
            limit=limit
        )

        return {
            "messages": [MessageResponse.model_validate(m) for m in messages],
            "total": total,
            "page": page,
            "limit": limit
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve messages")


@router.post("/sessions/{session_id}/messages", response_model=SendMessageResponse)
async def send_message(
    session_id: UUID,
    request: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a message and get AI response."""
    try:
        # Verify session ownership
        session_service = SessionService(db)
        session = session_service.get_session_by_id(session_id)

        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        if session.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to send messages in this session")

        # Send message and get response
        message_service = MessageService(db)
        user_message, assistant_response = message_service.send_message(
            session_id=session_id,
            user_id=current_user.id,
            content=request.content,
            message_type=request.message_type
        )

        db.commit()

        return {
            "user_message": MessageResponse.model_validate(user_message),
            "assistant_response": MessageResponse.model_validate(assistant_response)
        }
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to send message")
