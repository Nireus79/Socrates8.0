"""Audit log repository for audit trail data access."""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from backend.src.models import AuditLog
from backend.src.repositories.base_repository import BaseRepository


class AuditLogRepository(BaseRepository[AuditLog]):
    """Repository for AuditLog model."""

    def __init__(self, db: Session):
        """Initialize audit log repository."""
        super().__init__(db, AuditLog)

    def get_by_user(self, user_id: UUID) -> List[AuditLog]:
        """Get all audit logs by user.

        Args:
            user_id: User ID

        Returns:
            List of audit logs
        """
        return self.filter_by(user_id=user_id)

    def get_by_entity(self, entity_type: str, entity_id: UUID) -> List[AuditLog]:
        """Get audit logs for specific entity.

        Args:
            entity_type: Entity type (e.g., 'User', 'Project')
            entity_id: Entity ID

        Returns:
            List of audit logs
        """
        return self.db.query(AuditLog).filter(
            AuditLog.entity_type == entity_type,
            AuditLog.entity_id == entity_id
        ).all()

    def get_by_action(self, action: str) -> List[AuditLog]:
        """Get audit logs by action.

        Args:
            action: Action type (CREATE, UPDATE, DELETE)

        Returns:
            List of audit logs
        """
        return self.filter_by(action=action)

    def get_by_user_and_entity(
        self,
        user_id: UUID,
        entity_type: str,
        entity_id: UUID
    ) -> List[AuditLog]:
        """Get audit logs by user and entity.

        Args:
            user_id: User ID
            entity_type: Entity type
            entity_id: Entity ID

        Returns:
            List of audit logs
        """
        return self.db.query(AuditLog).filter(
            AuditLog.user_id == user_id,
            AuditLog.entity_type == entity_type,
            AuditLog.entity_id == entity_id
        ).all()

    def get_user_paginated(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[AuditLog], int]:
        """Get audit logs by user with pagination.

        Args:
            user_id: User ID
            skip: Number to skip
            limit: Limit

        Returns:
            Tuple of (audit logs, total count)
        """
        return self.filter_by_paginated(skip=skip, limit=limit, user_id=user_id)
