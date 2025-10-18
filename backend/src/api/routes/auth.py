"""Authentication API routes."""

import logging
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.services.user_service import UserService
from src.auth.jwt_handler import JWTHandler
from src.schemas.auth import RegisterRequest, LoginRequest, LoginResponse, TokenResponse
from src.config import settings
from datetime import timedelta

logger = logging.getLogger(__name__)

router = APIRouter(tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new user."""
    try:
        service = UserService(db)
        user = service.register_user(
            username=request.username,
            email=request.email,
            password=request.password,
            first_name=request.first_name,
            last_name=request.last_name
        )
        # User is already committed in service.register_user()

        return {
            "success": True,
            "data": {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "created_at": user.created_at.isoformat()
            },
            "message": "User created successfully"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        try:
            db.rollback()
        except:
            pass
        error_msg = f"{type(e).__name__}: {str(e)}"
        logger.error(f"Registration error: {error_msg}", exc_info=True)
        raise HTTPException(status_code=500, detail=error_msg)


@router.post("/login", response_model=dict)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Login user and return access token."""
    try:
        service = UserService(db)
        user = service.authenticate_user(request.username, request.password)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        access_token = JWTHandler.create_access_token(user.id)
        expires_in = settings.JWT_EXPIRE_MINUTES * 60

        return {
            "success": True,
            "data": {
                "user_id": str(user.id),
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "access_token": access_token,
                "token_type": "bearer",
                "expires_in": expires_in
            },
            "message": "Login successful"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Login failed")


@router.post("/logout")
async def logout():
    """Logout user (token invalidation handled client-side)."""
    return {
        "success": True,
        "message": "Logged out successfully"
    }


@router.post("/refresh", response_model=dict)
async def refresh_token(token: str):
    """Refresh access token."""
    try:
        user_id = JWTHandler.verify_token(token)

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        new_token = JWTHandler.create_access_token(user_id)
        expires_in = settings.JWT_EXPIRE_MINUTES * 60

        return {
            "success": True,
            "data": {
                "access_token": new_token,
                "token_type": "bearer",
                "expires_in": expires_in
            },
            "message": "Token refreshed"
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token refresh failed")
