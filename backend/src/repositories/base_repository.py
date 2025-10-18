"""Base repository with common CRUD operations."""

from typing import Generic, TypeVar, Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc

T = TypeVar('T')


class BaseRepository(Generic[T]):
    """Base repository with common CRUD operations."""

    def __init__(self, db: Session, model: type):
        """Initialize repository.

        Args:
            db: SQLAlchemy session
            model: SQLAlchemy model class
        """
        self.db = db
        self.model = model

    def create(self, obj_in: Dict[str, Any]) -> T:
        """Create a new record.

        Args:
            obj_in: Dictionary with object data

        Returns:
            Created object
        """
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        self.db.flush()
        return db_obj

    def get_by_id(self, obj_id: Any) -> Optional[T]:
        """Get record by ID.

        Args:
            obj_id: Object ID

        Returns:
            Object or None
        """
        return self.db.query(self.model).filter(self.model.id == obj_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all records with pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of objects
        """
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def get_all_sorted(
        self,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        skip: int = 0,
        limit: int = 100
    ) -> List[T]:
        """Get all records sorted.

        Args:
            sort_by: Field to sort by
            sort_order: 'asc' or 'desc'
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of sorted objects
        """
        query = self.db.query(self.model)

        if hasattr(self.model, sort_by):
            sort_field = getattr(self.model, sort_by)
            if sort_order.lower() == "asc":
                query = query.order_by(asc(sort_field))
            else:
                query = query.order_by(desc(sort_field))

        return query.offset(skip).limit(limit).all()

    def update(self, obj_id: Any, obj_in: Dict[str, Any]) -> Optional[T]:
        """Update a record.

        Args:
            obj_id: Object ID
            obj_in: Dictionary with updated data

        Returns:
            Updated object or None
        """
        db_obj = self.get_by_id(obj_id)
        if not db_obj:
            return None

        for key, value in obj_in.items():
            setattr(db_obj, key, value)

        self.db.flush()
        return db_obj

    def delete(self, obj_id: Any) -> bool:
        """Delete a record.

        Args:
            obj_id: Object ID

        Returns:
            True if deleted, False if not found
        """
        db_obj = self.get_by_id(obj_id)
        if not db_obj:
            return False

        self.db.delete(db_obj)
        self.db.flush()
        return True

    def count(self) -> int:
        """Count total records.

        Returns:
            Total count
        """
        return self.db.query(self.model).count()

    def filter_by(self, **kwargs) -> List[T]:
        """Filter records by attributes.

        Args:
            **kwargs: Filter conditions

        Returns:
            List of matching objects
        """
        query = self.db.query(self.model)
        for key, value in kwargs.items():
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == value)
        return query.all()

    def filter_by_paginated(
        self,
        skip: int = 0,
        limit: int = 100,
        **kwargs
    ) -> tuple[List[T], int]:
        """Filter records with pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            **kwargs: Filter conditions

        Returns:
            Tuple of (list of objects, total count)
        """
        query = self.db.query(self.model)
        for key, value in kwargs.items():
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == value)

        total = query.count()
        records = query.offset(skip).limit(limit).all()
        return records, total

    def exists(self, **kwargs) -> bool:
        """Check if record exists.

        Args:
            **kwargs: Filter conditions

        Returns:
            True if record exists
        """
        query = self.db.query(self.model)
        for key, value in kwargs.items():
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == value)
        return query.first() is not None

    def delete_all(self, **kwargs) -> int:
        """Delete all records matching conditions.

        Args:
            **kwargs: Filter conditions

        Returns:
            Number of deleted records
        """
        query = self.db.query(self.model)
        for key, value in kwargs.items():
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == value)

        count = query.count()
        query.delete()
        self.db.flush()
        return count
