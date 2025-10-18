"""Message model for conversation storage."""

import uuid
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, func, JSON
from sqlalchemy.orm import relationship

from backend.src.models.base import Base


class Message(Base):
    """Message model for user and assistant messages."""

    __tablename__ = "messages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(36), ForeignKey("sessions.id", ondelete="CASCADE"),
                       nullable=False, index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"),
                    nullable=False, index=True)
    role = Column(String(50), nullable=False, index=True)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    message_type = Column(String(50), default='text')
    meta = Column(JSON, default=dict)
    created_at = Column(DateTime, default=func.now(), index=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    session = relationship("Session", back_populates="messages")
    user = relationship("User", back_populates="messages")

    def __repr__(self):
        return f"<Message {self.role} in {self.session_id}>"
