"""Base service with common patterns."""

import logging
from typing import Dict, Any
from sqlalchemy.orm import Session


logger = logging.getLogger(__name__)


class BaseService:
    """Base service with common functionality."""

    def __init__(self, db: Session):
        """Initialize service.

        Args:
            db: SQLAlchemy session
        """
        self.db = db
        self.logger = logger

    def commit(self) -> None:
        """Commit transaction."""
        try:
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Commit failed: {e}")
            raise

    def rollback(self) -> None:
        """Rollback transaction."""
        self.db.rollback()

    def flush(self) -> None:
        """Flush session."""
        try:
            self.db.flush()
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Flush failed: {e}")
            raise

    def handle_error(self, error: Exception, context: str) -> None:
        """Handle and log error.

        Args:
            error: The exception
            context: Context string for logging

        Raises:
            The original exception after logging
        """
        self.logger.error(f"{context}: {str(error)}")
        self.rollback()
        raise
