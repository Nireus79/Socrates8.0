"""Project repository for project data access."""

from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session

from src.models import Project
from src.repositories.base_repository import BaseRepository


class ProjectRepository(BaseRepository[Project]):
    """Repository for Project model."""

    def __init__(self, db: Session):
        """Initialize project repository."""
        super().__init__(db, Project)

    def get_by_owner(self, owner_id: UUID) -> List[Project]:
        """Get all projects by owner.

        Args:
            owner_id: Owner user ID

        Returns:
            List of projects
        """
        return self.filter_by(owner_id=owner_id)

    def get_by_owner_and_status(self, owner_id: UUID, status: str) -> List[Project]:
        """Get projects by owner and status.

        Args:
            owner_id: Owner user ID
            status: Project status

        Returns:
            List of projects
        """
        return self.db.query(Project).filter(
            Project.owner_id == owner_id,
            Project.status == status
        ).all()

    def get_by_status(self, status: str) -> List[Project]:
        """Get all projects by status.

        Args:
            status: Project status

        Returns:
            List of projects
        """
        return self.filter_by(status=status)

    def get_by_owner_paginated(
        self,
        owner_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[Project], int]:
        """Get projects by owner with pagination.

        Args:
            owner_id: Owner user ID
            skip: Number to skip
            limit: Limit

        Returns:
            Tuple of (projects, total count)
        """
        return self.filter_by_paginated(skip=skip, limit=limit, owner_id=owner_id)
