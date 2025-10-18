"""User preferences model for settings management."""

import uuid
from sqlalchemy import Column, String, DateTime, Float, Integer, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship

from src.models.base import Base


class UserPreference(Base):
    """User preferences/settings model."""

    __tablename__ = "user_preferences"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"),
                    nullable=False, unique=True, index=True)
    theme = Column(String(50), default='dark')
    llm_model = Column(String(255), default='claude-3-sonnet')
    llm_temperature = Column(Float, default=0.7)
    llm_max_tokens = Column(Integer, default=2000)
    ide_type = Column(String(50))
    auto_sync = Column(Boolean, default=False)
    notifications_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", foreign_keys=[user_id])

    def __repr__(self):
        return f"<UserPreference {self.user_id}>"
