"""Document service for file management."""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from src.models import Document
from src.repositories import DocumentRepository
from src.services.base_service import BaseService


class DocumentService(BaseService):
    """Service for document management."""

    def __init__(self, db: Session):
        """Initialize document service."""
        super().__init__(db)
        self.repo = DocumentRepository(db)

    def upload_document(
        self,
        owner_id: UUID,
        filename: str,
        file_path: str,
        file_type: str = None,
        project_id: UUID = None,
        content_summary: str = None
    ) -> Document:
        """Upload document.

        Args:
            owner_id: Owner user ID
            filename: Original filename
            file_path: Path to stored file
            file_type: File type (pdf, docx, txt, etc.)
            project_id: Associated project ID
            content_summary: Content summary

        Returns:
            Created Document

        Raises:
            ValueError: If validation fails
        """
        if not filename or len(filename.strip()) == 0:
            raise ValueError("Filename is required")

        if not file_path or len(file_path.strip()) == 0:
            raise ValueError("File path is required")

        document = Document(
            owner_id=owner_id,
            filename=filename,
            file_path=file_path,
            file_type=file_type,
            project_id=project_id,
            content_summary=content_summary,
            status="PROCESSED"
        )

        self.db.add(document)
        self.commit()

        self.logger.info(f"Document uploaded: {filename} by {owner_id}")
        return document

    def get_document(self, document_id: UUID, owner_id: UUID = None) -> Optional[Document]:
        """Get document by ID.

        Args:
            document_id: Document ID
            owner_id: Optional owner ID for authorization

        Returns:
            Document or None

        Raises:
            ValueError: If not authorized
        """
        doc = self.repo.get_by_id(document_id)

        if not doc:
            return None

        if owner_id and doc.owner_id != owner_id:
            raise ValueError("Not authorized to access this document")

        return doc

    def get_user_documents(self, owner_id: UUID) -> List[Document]:
        """Get all documents for user.

        Args:
            owner_id: Owner user ID

        Returns:
            List of documents
        """
        return self.repo.get_by_owner(owner_id)

    def get_project_documents(self, project_id: UUID) -> List[Document]:
        """Get documents for project.

        Args:
            project_id: Project ID

        Returns:
            List of documents
        """
        return self.repo.get_by_project(project_id)

    def delete_document(self, document_id: UUID, owner_id: UUID) -> bool:
        """Delete document.

        Args:
            document_id: Document ID
            owner_id: Owner user ID

        Returns:
            True if deleted

        Raises:
            ValueError: If authorization fails
        """
        doc = self.repo.get_by_id(document_id)

        if not doc:
            raise ValueError("Document not found")

        if doc.owner_id != owner_id:
            raise ValueError("Not authorized to delete this document")

        self.db.delete(doc)
        self.commit()

        self.logger.info(f"Document deleted: {document_id}")
        return True

    def set_vector_id(self, document_id: UUID, vector_id: str) -> Document:
        """Set vector ID for document (after RAG processing).

        Args:
            document_id: Document ID
            vector_id: Vector ID from embedding service

        Returns:
            Updated Document

        Raises:
            ValueError: If document not found
        """
        doc = self.repo.get_by_id(document_id)

        if not doc:
            raise ValueError("Document not found")

        doc.vector_id = vector_id
        self.commit()

        self.logger.info(f"Vector ID set for document: {document_id}")
        return doc
