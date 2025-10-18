"""Profile and settings API routes."""

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from backend.src.database import get_db
from backend.src.services.user_service import UserService
from backend.src.services.preference_service import PreferenceService
from backend.src.dependencies import get_current_user
from backend.src.schemas.profile import (
    ProfileResponse, ProfileUpdate, ChangePasswordRequest,
    PreferenceResponse, PreferenceUpdate
)
from backend.src.models.user import User

router = APIRouter(tags=["profile"])


@router.get("/profile", response_model=dict)
async def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's profile."""
    try:
        return {
            "success": True,
            "data": ProfileResponse.model_validate(current_user),
            "message": "Profile retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve profile")


@router.put("/profile", response_model=dict)
async def update_profile(
    request: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user's profile."""
    try:
        service = UserService(db)

        # Update profile fields
        if request.first_name is not None:
            current_user.first_name = request.first_name
        if request.last_name is not None:
            current_user.last_name = request.last_name
        if request.bio is not None:
            current_user.bio = request.bio
        if request.avatar_url is not None:
            current_user.avatar_url = request.avatar_url

        db.commit()
        db.refresh(current_user)

        return {
            "success": True,
            "data": ProfileResponse.model_validate(current_user),
            "message": "Profile updated successfully"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update profile")


@router.post("/profile/password", response_model=dict)
async def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change current user's password."""
    try:
        service = UserService(db)

        # Verify current password
        if not service.verify_password(request.current_password, current_user.hashed_password):
            raise HTTPException(status_code=401, detail="Current password is incorrect")

        # Validate new password matches confirmation
        if request.new_password != request.confirm_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")

        # Validate password strength
        if len(request.new_password) < 8:
            raise HTTPException(status_code=400, detail="Password must be at least 8 characters")

        # Update password
        current_user.hashed_password = service.hash_password(request.new_password)
        db.commit()

        return {
            "success": True,
            "data": None,
            "message": "Password changed successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to change password")


@router.get("/settings", response_model=dict)
async def get_settings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's preferences/settings."""
    try:
        service = PreferenceService(db)
        preferences = service.get_preferences(current_user.id)

        if not preferences:
            # Return default preferences if none exist
            preferences = service.create_default_preferences(current_user.id)
            db.commit()

        return {
            "success": True,
            "data": PreferenceResponse.model_validate(preferences),
            "message": "Settings retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve settings")


@router.put("/settings", response_model=dict)
async def update_settings(
    request: PreferenceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user's preferences/settings."""
    try:
        service = PreferenceService(db)
        preferences = service.get_preferences(current_user.id)

        if not preferences:
            # Create default preferences if they don't exist
            preferences = service.create_default_preferences(current_user.id)

        # Update fields
        if request.theme is not None:
            preferences.theme = request.theme
        if request.llm_model is not None:
            preferences.llm_model = request.llm_model
        if request.llm_temperature is not None:
            preferences.llm_temperature = request.llm_temperature
        if request.llm_max_tokens is not None:
            preferences.llm_max_tokens = request.llm_max_tokens
        if request.ide_type is not None:
            preferences.ide_type = request.ide_type
        if request.auto_sync is not None:
            preferences.auto_sync = request.auto_sync
        if request.notifications_enabled is not None:
            preferences.notifications_enabled = request.notifications_enabled

        db.commit()
        db.refresh(preferences)

        return {
            "success": True,
            "data": PreferenceResponse.model_validate(preferences),
            "message": "Settings updated successfully"
        }
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update settings")
