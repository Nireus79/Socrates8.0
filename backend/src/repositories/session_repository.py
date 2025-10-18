"""Session repository for session data access."""

from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session

from src.models import Session as SessionModel
from src.repositories.base_repository import BaseRepository


class SessionRepository(BaseRepository[SessionModel]):
    """Repository for Session model."""

    def __init__(self, db: Session):
        """Initialize session repository."""
        super().__init__(db, SessionModel)

    def get_by_owner(self, owner_id: UUID) -> List[SessionModel]:
        """Get all sessions by owner.

        Args:
            owner_id: Owner user ID

        Returns:
            List of sessions
        """
        return self.filter_by(owner_id=owner_id)

    def get_by_project(self, project_id: UUID) -> List[SessionModel]:
        """Get all sessions by project.

        Args:
            project_id: Project ID

        Returns:
            List of sessions
        """
        return self.filter_by(project_id=project_id)

    def get_by_owner_and_status(self, owner_id: UUID, status: str) -> List[SessionModel]:
        """Get sessions by owner and status.

        Args:
            owner_id: Owner user ID
            status: Session status

        Returns:
            List of sessions
        """
        return self.db.query(SessionModel).filter(
            SessionModel.owner_id == owner_id,
            SessionModel.status == status
        ).all()

    def get_active_sessions(self, owner_id: UUID) -> List[SessionModel]:
        """Get active sessions for user.

        Args:
            owner_id: Owner user ID

        Returns:
            List of active sessions
        """
        return self.get_by_owner_and_status(owner_id, "ACTIVE")

    def get_by_owner_paginated(
        self,
        owner_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[SessionModel], int]:
        """Get sessions by owner with pagination.

        Args:
            owner_id: Owner user ID
            skip: Number to skip
            limit: Limit

        Returns:
            Tuple of (sessions, total count)
        """
        return self.filter_by_paginated(skip=skip, limit=limit, owner_id=owner_id)
