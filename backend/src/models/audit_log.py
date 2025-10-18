"""Audit log model for change tracking."""

import uuid
from sqlalchemy import Column, String, DateTime, func, ForeignKey, JSON
from sqlalchemy.orm import relationship

from backend.src.models.base import Base


class AuditLog(Base):
    """Audit log model for tracking changes."""

    __tablename__ = "audit_log"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"),
                    index=True)
    entity_type = Column(String(100))
    entity_id = Column(String(36))
    action = Column(String(50))  # CREATE, UPDATE, DELETE
    old_value = Column(JSON)
    new_value = Column(JSON)
    created_at = Column(DateTime, default=func.now(), index=True)

    def __repr__(self):
        return f"<AuditLog {self.action} {self.entity_type}>"
