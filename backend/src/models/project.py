"""Project model for project management."""

import uuid
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, func, JSON
from sqlalchemy.orm import relationship

from src.models.base import Base


class Project(Base):
    """Project model."""

    __tablename__ = "projects"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"),
                     nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(50), default='PLANNING', index=True)
    technology_stack = Column(JSON, default=list)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    owner = relationship("User", back_populates="projects")
    sessions = relationship("Session", back_populates="project", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="project")

    def __repr__(self):
        return f"<Project {self.name}>"
