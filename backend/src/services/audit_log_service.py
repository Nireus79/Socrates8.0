"""Audit log service for change tracking."""

from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session

from backend.src.models import AuditLog
from backend.src.repositories import AuditLogRepository
from backend.src.services.base_service import BaseService


class AuditLogService(BaseService):
    """Service for audit trail."""

    def __init__(self, db: Session):
        """Initialize audit log service."""
        super().__init__(db)
        self.repo = AuditLogRepository(db)

    def log_create(
        self,
        user_id: UUID,
        entity_type: str,
        entity_id: UUID,
        new_value: Dict[str, Any] = None
    ) -> AuditLog:
        """Log entity creation.

        Args:
            user_id: User performing action
            entity_type: Type of entity (User, Project, etc.)
            entity_id: Entity ID
            new_value: New entity data

        Returns:
            Created AuditLog
        """
        log = AuditLog(
            user_id=user_id,
            entity_type=entity_type,
            entity_id=entity_id,
            action="CREATE",
            new_value=new_value or {}
        )

        self.db.add(log)
        self.flush()

        self.logger.info(f"Audit log created: {entity_type} {entity_id}")
        return log

    def log_update(
        self,
        user_id: UUID,
        entity_type: str,
        entity_id: UUID,
        old_value: Dict[str, Any] = None,
        new_value: Dict[str, Any] = None
    ) -> AuditLog:
        """Log entity update.

        Args:
            user_id: User performing action
            entity_type: Type of entity
            entity_id: Entity ID
            old_value: Previous entity data
            new_value: New entity data

        Returns:
            Created AuditLog
        """
        log = AuditLog(
            user_id=user_id,
            entity_type=entity_type,
            entity_id=entity_id,
            action="UPDATE",
            old_value=old_value or {},
            new_value=new_value or {}
        )

        self.db.add(log)
        self.flush()

        self.logger.info(f"Audit log updated: {entity_type} {entity_id}")
        return log

    def log_delete(
        self,
        user_id: UUID,
        entity_type: str,
        entity_id: UUID,
        old_value: Dict[str, Any] = None
    ) -> AuditLog:
        """Log entity deletion.

        Args:
            user_id: User performing action
            entity_type: Type of entity
            entity_id: Entity ID
            old_value: Deleted entity data

        Returns:
            Created AuditLog
        """
        log = AuditLog(
            user_id=user_id,
            entity_type=entity_type,
            entity_id=entity_id,
            action="DELETE",
            old_value=old_value or {}
        )

        self.db.add(log)
        self.flush()

        self.logger.info(f"Audit log deleted: {entity_type} {entity_id}")
        return log

    def get_user_audit_logs(self, user_id: UUID) -> List[AuditLog]:
        """Get audit logs for user.

        Args:
            user_id: User ID

        Returns:
            List of audit logs
        """
        return self.repo.get_by_user(user_id)

    def get_entity_audit_logs(self, entity_type: str, entity_id: UUID) -> List[AuditLog]:
        """Get audit logs for entity.

        Args:
            entity_type: Type of entity
            entity_id: Entity ID

        Returns:
            List of audit logs
        """
        return self.repo.get_by_entity(entity_type, entity_id)

    def get_action_logs(self, action: str) -> List[AuditLog]:
        """Get logs by action.

        Args:
            action: Action type (CREATE, UPDATE, DELETE)

        Returns:
            List of audit logs
        """
        return self.repo.get_by_action(action)
