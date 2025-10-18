"""Preference repository for user preferences data access."""

from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session

from src.models import UserPreference
from src.repositories.base_repository import BaseRepository


class PreferenceRepository(BaseRepository[UserPreference]):
    """Repository for UserPreference model."""

    def __init__(self, db: Session):
        """Initialize preference repository."""
        super().__init__(db, UserPreference)

    def get_by_user_id(self, user_id: UUID) -> Optional[UserPreference]:
        """Get preferences by user ID.

        Args:
            user_id: User ID

        Returns:
            UserPreference or None
        """
        return self.db.query(UserPreference).filter(
            UserPreference.user_id == user_id
        ).first()

    def create_for_user(self, user_id: UUID) -> UserPreference:
        """Create default preferences for user.

        Args:
            user_id: User ID

        Returns:
            Created UserPreference
        """
        prefs = UserPreference(user_id=user_id)
        self.db.add(prefs)
        self.db.flush()
        return prefs
