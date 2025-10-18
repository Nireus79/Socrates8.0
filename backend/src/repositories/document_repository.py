"""Document repository for document data access."""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from backend.src.models import Document
from backend.src.repositories.base_repository import BaseRepository


class DocumentRepository(BaseRepository[Document]):
    """Repository for Document model."""

    def __init__(self, db: Session):
        """Initialize document repository."""
        super().__init__(db, Document)

    def get_by_owner(self, owner_id: UUID) -> List[Document]:
        """Get all documents by owner.

        Args:
            owner_id: Owner user ID

        Returns:
            List of documents
        """
        return self.filter_by(owner_id=owner_id)

    def get_by_project(self, project_id: UUID) -> List[Document]:
        """Get all documents by project.

        Args:
            project_id: Project ID

        Returns:
            List of documents
        """
        return self.filter_by(project_id=project_id)

    def get_by_owner_and_project(
        self,
        owner_id: UUID,
        project_id: UUID
    ) -> List[Document]:
        """Get documents by owner and project.

        Args:
            owner_id: Owner user ID
            project_id: Project ID

        Returns:
            List of documents
        """
        return self.db.query(Document).filter(
            Document.owner_id == owner_id,
            Document.project_id == project_id
        ).all()

    def get_by_status(self, status: str) -> List[Document]:
        """Get documents by status.

        Args:
            status: Document status

        Returns:
            List of documents
        """
        return self.filter_by(status=status)

    def get_by_vector_id(self, vector_id: str) -> Optional[Document]:
        """Get document by vector ID.

        Args:
            vector_id: Vector ID from ChromaDB

        Returns:
            Document or None
        """
        return self.db.query(Document).filter(
            Document.vector_id == vector_id
        ).first()

    def get_by_owner_paginated(
        self,
        owner_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[Document], int]:
        """Get documents by owner with pagination.

        Args:
            owner_id: Owner user ID
            skip: Number to skip
            limit: Limit

        Returns:
            Tuple of (documents, total count)
        """
        return self.filter_by_paginated(skip=skip, limit=limit, owner_id=owner_id)
