"""Database configuration and session management."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from src.config import settings

# Create database engine
if settings.DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=False,
    )
else:
    engine = create_engine(
        settings.DATABASE_URL,
        poolclass=NullPool,
        echo=False,
    )

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=True,  # Changed to True for SQLite compatibility
    bind=engine,
    expire_on_commit=False,  # Keep objects after commit
)


def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
