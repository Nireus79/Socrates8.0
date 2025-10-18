"""Session model for chat session management."""

import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from src.models.base import Base


class Session(Base):
    """Session model for Socratic questioning sessions."""

    __tablename__ = "sessions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"),
                     nullable=False, index=True)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="SET NULL"),
                       index=True)
    name = Column(String(255))
    status = Column(String(50), default='ACTIVE', index=True)
    mode = Column(String(50), default='chat')
    role = Column(String(100))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    archived_at = Column(DateTime)

    # Relationships
    owner = relationship("User", back_populates="sessions")
    project = relationship("Project", back_populates="sessions")
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Session {self.id}>"
