"""Session API routes."""

from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
from uuid import UUID

from backend.src.database import get_db
from backend.src.services.session_service import SessionService
from backend.src.dependencies import get_current_user
from backend.src.schemas.session import (
    SessionCreate, SessionUpdate, SessionToggleMode, SessionResponse, SessionListResponse
)
from backend.src.models.user import User

router = APIRouter(tags=["sessions"])


@router.get("/sessions", response_model=SessionListResponse)
async def list_sessions(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    project_id: UUID = Query(None),
    status_filter: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List sessions owned by current user with pagination."""
    try:
        service = SessionService(db)

        # Get total count
        total = service.count_sessions(owner_id=current_user.id, project_id=project_id)

        # Get paginated sessions
        sessions = service.get_sessions_paginated(
            owner_id=current_user.id,
            project_id=project_id,
            page=page,
            limit=limit,
            status=status_filter
        )

        return {
            "sessions": [SessionResponse.model_validate(s) for s in sessions],
            "total": total,
            "page": page,
            "limit": limit
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to list sessions")


@router.post("/sessions", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_session(
    request: SessionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new session."""
    try:
        service = SessionService(db)
        session = service.create_session(
            name=request.name,
            mode=request.mode,
            project_id=request.project_id,
            owner_id=current_user.id,
            role=request.role
        )
        db.commit()

        return {
            "success": True,
            "data": SessionResponse.model_validate(session),
            "message": "Session created successfully"
        }
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create session")


@router.get("/sessions/{session_id}", response_model=dict)
async def get_session(
    session_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get session details with message count."""
    try:
        service = SessionService(db)
        session = service.get_session_by_id(session_id)

        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        # Check authorization
        if session.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to view this session")

        return {
            "success": True,
            "data": SessionResponse.model_validate(session),
            "message": "Session retrieved successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve session")


@router.put("/sessions/{session_id}", response_model=dict)
async def update_session(
    session_id: UUID,
    request: SessionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update session details."""
    try:
        service = SessionService(db)
        session = service.get_session_by_id(session_id)

        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        # Check authorization
        if session.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to update this session")

        # Update fields
        if request.name is not None:
            session.name = request.name
        if request.mode is not None:
            session.mode = request.mode
        if request.status is not None:
            session.status = request.status

        db.commit()
        db.refresh(session)

        return {
            "success": True,
            "data": SessionResponse.model_validate(session),
            "message": "Session updated successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update session")


@router.post("/sessions/{session_id}/toggle-mode", response_model=dict)
async def toggle_session_mode(
    session_id: UUID,
    request: SessionToggleMode,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Toggle session mode (chat, question, teaching, review)."""
    try:
        service = SessionService(db)
        session = service.get_session_by_id(session_id)

        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        # Check authorization
        if session.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to update this session")

        # Validate mode
        if request.mode not in ["chat", "question", "teaching", "review"]:
            raise HTTPException(status_code=400, detail="Invalid mode")

        # Update mode
        session.mode = request.mode
        db.commit()
        db.refresh(session)

        return {
            "success": True,
            "data": SessionResponse.model_validate(session),
            "message": f"Session mode changed to {request.mode}"
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to toggle session mode")


@router.delete("/sessions/{session_id}", response_model=dict)
async def delete_session(
    session_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a session and its associated messages."""
    try:
        service = SessionService(db)
        session = service.get_session_by_id(session_id)

        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        # Check authorization
        if session.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this session")

        # Delete session (cascade will delete messages)
        service.delete_session(session_id)
        db.commit()

        return {
            "success": True,
            "data": None,
            "message": "Session deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete session")
