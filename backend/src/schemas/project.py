"""Pydantic schemas for project endpoints."""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class ProjectCreate(BaseModel):
    """Create project request."""

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    technology_stack: Optional[List[str]] = None


class ProjectUpdate(BaseModel):
    """Update project request."""

    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    status: Optional[str] = None
    technology_stack: Optional[List[str]] = None


class ProjectResponse(BaseModel):
    """Project response."""

    id: str
    name: str
    description: Optional[str]
    status: str
    technology_stack: List[str]
    owner_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProjectListResponse(BaseModel):
    """List of projects response."""

    projects: List[ProjectResponse]
    total: int
    page: int
    limit: int
