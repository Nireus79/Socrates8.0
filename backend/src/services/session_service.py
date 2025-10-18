"""Session service for session management."""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import func

from src.models import Session as SessionModel
from src.repositories import SessionRepository, MessageRepository
from src.services.base_service import BaseService


class SessionService(BaseService):
    """Service for session management."""

    def __init__(self, db: Session):
        """Initialize session service."""
        super().__init__(db)
        self.session_repo = SessionRepository(db)
        self.message_repo = MessageRepository(db)

    def create_session(
        self,
        owner_id: UUID,
        project_id: UUID = None,
        name: str = None,
        mode: str = "chat",
        role: str = None
    ) -> SessionModel:
        """Create new session.

        Args:
            owner_id: Owner user ID
            project_id: Project ID (optional)
            name: Session name
            mode: Session mode (chat, question, teaching, review)
            role: User role in session

        Returns:
            Created session

        Raises:
            ValueError: If validation fails
        """
        valid_modes = ["chat", "question", "teaching", "review"]
        if mode not in valid_modes:
            raise ValueError(f"Invalid mode. Must be one of: {', '.join(valid_modes)}")

        session = SessionModel(
            owner_id=owner_id,
            project_id=project_id,
            name=name,
            mode=mode,
            role=role,
            status="ACTIVE"
        )

        self.db.add(session)
        self.commit()

        self.logger.info(f"Session created: {session.id} by {owner_id}")
        return session

    def get_session(self, session_id: UUID, owner_id: UUID = None) -> Optional[SessionModel]:
        """Get session by ID.

        Args:
            session_id: Session ID
            owner_id: Optional owner ID for authorization

        Returns:
            Session or None

        Raises:
            ValueError: If not authorized
        """
        session = self.session_repo.get_by_id(session_id)

        if not session:
            return None

        if owner_id and session.owner_id != owner_id:
            raise ValueError("Not authorized to access this session")

        return session

    def get_user_sessions(self, owner_id: UUID, status: str = None) -> List[SessionModel]:
        """Get user sessions.

        Args:
            owner_id: Owner user ID
            status: Optional status filter

        Returns:
            List of sessions
        """
        if status:
            return self.session_repo.get_by_owner_and_status(owner_id, status)
        return self.session_repo.get_by_owner(owner_id)

    def get_project_sessions(self, project_id: UUID) -> List[SessionModel]:
        """Get sessions for project.

        Args:
            project_id: Project ID

        Returns:
            List of sessions
        """
        return self.session_repo.get_by_project(project_id)

    def toggle_mode(self, session_id: UUID, owner_id: UUID, new_mode: str) -> SessionModel:
        """Change session mode.

        Args:
            session_id: Session ID
            owner_id: Owner user ID
            new_mode: New mode

        Returns:
            Updated session

        Raises:
            ValueError: If validation fails
        """
        session = self.get_session(session_id, owner_id)

        if not session:
            raise ValueError("Session not found")

        valid_modes = ["chat", "question", "teaching", "review"]
        if new_mode not in valid_modes:
            raise ValueError(f"Invalid mode. Must be one of: {', '.join(valid_modes)}")

        session.mode = new_mode
        self.commit()

        self.logger.info(f"Session mode changed: {session_id} -> {new_mode}")
        return session

    def archive_session(self, session_id: UUID, owner_id: UUID) -> SessionModel:
        """Archive session.

        Args:
            session_id: Session ID
            owner_id: Owner user ID

        Returns:
            Updated session

        Raises:
            ValueError: If validation fails
        """
        session = self.get_session(session_id, owner_id)

        if not session:
            raise ValueError("Session not found")

        session.status = "ARCHIVED"
        session.archived_at = func.now()
        self.commit()

        self.logger.info(f"Session archived: {session_id}")
        return session

    def delete_session(self, session_id: UUID, owner_id: UUID) -> bool:
        """Delete session.

        Args:
            session_id: Session ID
            owner_id: Owner user ID

        Returns:
            True if deleted

        Raises:
            ValueError: If authorization fails
        """
        session = self.session_repo.get_by_id(session_id)

        if not session:
            raise ValueError("Session not found")

        if session.owner_id != owner_id:
            raise ValueError("Not authorized to delete this session")

        self.db.delete(session)
        self.commit()

        self.logger.info(f"Session deleted: {session_id}")
        return True

    def get_session_message_count(self, session_id: UUID) -> int:
        """Get message count for session.

        Args:
            session_id: Session ID

        Returns:
            Message count
        """
        return self.message_repo.get_by_session_count(session_id)
