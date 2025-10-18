"""Project service for project management."""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from src.models import Project
from src.repositories import ProjectRepository
from src.services.base_service import BaseService


class ProjectService(BaseService):
    """Service for project management."""

    def __init__(self, db: Session):
        """Initialize project service."""
        super().__init__(db)
        self.repo = ProjectRepository(db)

    def create_project(
        self,
        owner_id: UUID,
        name: str,
        description: str = None,
        technology_stack: List[str] = None
    ) -> Project:
        """Create new project.

        Args:
            owner_id: Owner user ID
            name: Project name
            description: Project description
            technology_stack: List of technologies

        Returns:
            Created project

        Raises:
            ValueError: If validation fails
        """
        if not name or len(name.strip()) == 0:
            raise ValueError("Project name is required")

        if len(name) > 255:
            raise ValueError("Project name too long (max 255 characters)")

        project = Project(
            owner_id=owner_id,
            name=name,
            description=description,
            technology_stack=technology_stack or [],
            status="PLANNING"
        )

        self.db.add(project)
        self.commit()

        self.logger.info(f"Project created: {name} by {owner_id}")
        return project

    def get_project(self, project_id: UUID, owner_id: UUID = None) -> Optional[Project]:
        """Get project by ID.

        Args:
            project_id: Project ID
            owner_id: Optional owner ID for authorization check

        Returns:
            Project or None

        Raises:
            ValueError: If not authorized
        """
        project = self.repo.get_by_id(project_id)

        if not project:
            return None

        if owner_id and project.owner_id != owner_id:
            raise ValueError("Not authorized to access this project")

        return project

    def get_user_projects(self, owner_id: UUID, status: str = None) -> List[Project]:
        """Get all projects for user.

        Args:
            owner_id: Owner user ID
            status: Optional status filter

        Returns:
            List of projects
        """
        if status:
            return self.repo.get_by_owner_and_status(owner_id, status)
        return self.repo.get_by_owner(owner_id)

    def update_project(
        self,
        project_id: UUID,
        owner_id: UUID,
        name: str = None,
        description: str = None,
        status: str = None,
        technology_stack: List[str] = None
    ) -> Project:
        """Update project.

        Args:
            project_id: Project ID
            owner_id: Owner user ID (for authorization)
            name: New name
            description: New description
            status: New status
            technology_stack: New technology stack

        Returns:
            Updated project

        Raises:
            ValueError: If validation fails
        """
        project = self.repo.get_by_id(project_id)

        if not project:
            raise ValueError("Project not found")

        if project.owner_id != owner_id:
            raise ValueError("Not authorized to update this project")

        if name:
            if len(name) > 255:
                raise ValueError("Project name too long")
            project.name = name

        if description is not None:
            project.description = description

        if status:
            valid_statuses = ["PLANNING", "DESIGN", "DEVELOPMENT", "TESTING", "COMPLETE"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
            project.status = status

        if technology_stack is not None:
            project.technology_stack = technology_stack

        self.commit()
        self.logger.info(f"Project updated: {project_id}")
        return project

    def delete_project(self, project_id: UUID, owner_id: UUID) -> bool:
        """Delete project.

        Args:
            project_id: Project ID
            owner_id: Owner user ID (for authorization)

        Returns:
            True if deleted

        Raises:
            ValueError: If authorization fails
        """
        project = self.repo.get_by_id(project_id)

        if not project:
            raise ValueError("Project not found")

        if project.owner_id != owner_id:
            raise ValueError("Not authorized to delete this project")

        self.db.delete(project)
        self.commit()

        self.logger.info(f"Project deleted: {project_id}")
        return True

    def get_projects_by_status(self, status: str) -> List[Project]:
        """Get all projects by status.

        Args:
            status: Project status

        Returns:
            List of projects
        """
        return self.repo.get_by_status(status)
