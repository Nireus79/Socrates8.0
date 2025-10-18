"""Message repository for message data access."""

from typing import List
from uuid import UUID
from sqlalchemy.orm import Session

from backend.src.models import Message
from backend.src.repositories.base_repository import BaseRepository


class MessageRepository(BaseRepository[Message]):
    """Repository for Message model."""

    def __init__(self, db: Session):
        """Initialize message repository."""
        super().__init__(db, Message)

    def get_by_session(
        self,
        session_id: UUID,
        skip: int = 0,
        limit: int = 50
    ) -> List[Message]:
        """Get messages by session with pagination.

        Args:
            session_id: Session ID
            skip: Number to skip
            limit: Limit

        Returns:
            List of messages
        """
        return self.db.query(Message).filter(
            Message.session_id == session_id
        ).offset(skip).limit(limit).all()

    def get_by_session_sorted(
        self,
        session_id: UUID,
        skip: int = 0,
        limit: int = 50,
        sort_order: str = "asc"
    ) -> List[Message]:
        """Get messages by session sorted.

        Args:
            session_id: Session ID
            skip: Number to skip
            limit: Limit
            sort_order: 'asc' or 'desc'

        Returns:
            List of messages sorted
        """
        from sqlalchemy import asc, desc
        query = self.db.query(Message).filter(Message.session_id == session_id)

        if sort_order.lower() == "desc":
            query = query.order_by(desc(Message.created_at))
        else:
            query = query.order_by(asc(Message.created_at))

        return query.offset(skip).limit(limit).all()

    def get_by_session_count(self, session_id: UUID) -> int:
        """Get message count for session.

        Args:
            session_id: Session ID

        Returns:
            Message count
        """
        return self.db.query(Message).filter(
            Message.session_id == session_id
        ).count()

    def get_by_user_and_session(
        self,
        session_id: UUID,
        user_id: UUID
    ) -> List[Message]:
        """Get messages by session and user.

        Args:
            session_id: Session ID
            user_id: User ID

        Returns:
            List of messages
        """
        return self.db.query(Message).filter(
            Message.session_id == session_id,
            Message.user_id == user_id
        ).all()

    def get_by_role(self, session_id: UUID, role: str) -> List[Message]:
        """Get messages by session and role.

        Args:
            session_id: Session ID
            role: Message role ('user' or 'assistant')

        Returns:
            List of messages
        """
        return self.db.query(Message).filter(
            Message.session_id == session_id,
            Message.role == role
        ).all()
