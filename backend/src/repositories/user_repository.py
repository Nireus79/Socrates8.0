"""User repository for user data access."""

from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session

from backend.src.models import User
from backend.src.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for User model."""

    def __init__(self, db: Session):
        """Initialize user repository."""
        super().__init__(db, User)

    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username.

        Args:
            username: Username

        Returns:
            User or None
        """
        return self.db.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email.

        Args:
            email: Email address

        Returns:
            User or None
        """
        return self.db.query(User).filter(User.email == email).first()

    def get_by_status(self, status: str):
        """Get all users by status.

        Args:
            status: User status (ACTIVE, INACTIVE, SUSPENDED)

        Returns:
            List of users
        """
        return self.filter_by(status=status)

    def get_active_users(self):
        """Get all active users.

        Returns:
            List of active users
        """
        return self.get_by_status("ACTIVE")
