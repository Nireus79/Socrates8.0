"""Document model for file management and RAG."""

import uuid
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, func
from sqlalchemy.orm import relationship

from src.models.base import Base


class Document(Base):
    """Document model for uploaded files and RAG integration."""

    __tablename__ = "documents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"),
                     nullable=False, index=True)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="SET NULL"),
                       index=True)
    filename = Column(String(500), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(50))
    content_summary = Column(Text)
    vector_id = Column(String(500))
    status = Column(String(50), default='PROCESSED', index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    owner = relationship("User", foreign_keys=[owner_id])
    project = relationship("Project", back_populates="documents")

    def __repr__(self):
        return f"<Document {self.filename}>"
