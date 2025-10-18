"""Preference service for user settings."""

from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session

from backend.src.models import UserPreference
from backend.src.repositories import PreferenceRepository
from backend.src.services.base_service import BaseService


class PreferenceService(BaseService):
    """Service for user preferences."""

    def __init__(self, db: Session):
        """Initialize preference service."""
        super().__init__(db)
        self.repo = PreferenceRepository(db)

    def get_or_create_preferences(self, user_id: UUID) -> UserPreference:
        """Get preferences or create with defaults.

        Args:
            user_id: User ID

        Returns:
            UserPreference
        """
        prefs = self.repo.get_by_user_id(user_id)

        if not prefs:
            prefs = self.repo.create_for_user(user_id)
            self.commit()
            self.logger.info(f"Default preferences created for user: {user_id}")

        return prefs

    def get_preferences(self, user_id: UUID) -> Optional[UserPreference]:
        """Get user preferences.

        Args:
            user_id: User ID

        Returns:
            UserPreference or None
        """
        return self.repo.get_by_user_id(user_id)

    def update_preferences(
        self,
        user_id: UUID,
        theme: str = None,
        llm_model: str = None,
        llm_temperature: float = None,
        llm_max_tokens: int = None,
        ide_type: str = None,
        auto_sync: bool = None,
        notifications_enabled: bool = None
    ) -> UserPreference:
        """Update user preferences.

        Args:
            user_id: User ID
            theme: UI theme (light/dark)
            llm_model: LLM model name
            llm_temperature: LLM temperature (0.0-1.0)
            llm_max_tokens: Max tokens for LLM
            ide_type: IDE type
            auto_sync: Enable auto sync
            notifications_enabled: Enable notifications

        Returns:
            Updated UserPreference

        Raises:
            ValueError: If validation fails
        """
        prefs = self.get_or_create_preferences(user_id)

        if theme is not None:
            if theme not in ["light", "dark"]:
                raise ValueError("Theme must be 'light' or 'dark'")
            prefs.theme = theme

        if llm_model is not None:
            prefs.llm_model = llm_model

        if llm_temperature is not None:
            if not (0.0 <= llm_temperature <= 1.0):
                raise ValueError("Temperature must be between 0.0 and 1.0")
            prefs.llm_temperature = llm_temperature

        if llm_max_tokens is not None:
            if llm_max_tokens < 1:
                raise ValueError("Max tokens must be greater than 0")
            prefs.llm_max_tokens = llm_max_tokens

        if ide_type is not None:
            prefs.ide_type = ide_type

        if auto_sync is not None:
            prefs.auto_sync = auto_sync

        if notifications_enabled is not None:
            prefs.notifications_enabled = notifications_enabled

        self.commit()
        self.logger.info(f"Preferences updated for user: {user_id}")
        return prefs

    def reset_to_defaults(self, user_id: UUID) -> UserPreference:
        """Reset preferences to defaults.

        Args:
            user_id: User ID

        Returns:
            Reset UserPreference
        """
        prefs = self.get_or_create_preferences(user_id)

        prefs.theme = "dark"
        prefs.llm_model = "claude-3-sonnet"
        prefs.llm_temperature = 0.7
        prefs.llm_max_tokens = 2000
        prefs.ide_type = None
        prefs.auto_sync = False
        prefs.notifications_enabled = True

        self.commit()
        self.logger.info(f"Preferences reset to defaults for user: {user_id}")
        return prefs
