"""Seed database with test data."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import uuid
from src.database import SessionLocal, engine
from src.models import Base, User, Project, Session, Message, UserPreference
from src.config import settings
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash password."""
    return pwd_context.hash(password)


def seed():
    """Seed database with test data."""
    # Create tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Check if data already exists
        existing_user = db.query(User).filter_by(username="testuser").first()
        if existing_user:
            print("Test data already exists")
            return

        # Create test user
        user = User(
            id=uuid.uuid4(),
            username="testuser",
            email="test@example.com",
            password_hash=hash_password("Test@1234"),
            first_name="Test",
            last_name="User",
            bio="Test user for Socrates 8.0",
            status="ACTIVE"
        )
        db.add(user)
        db.flush()

        # Create test preferences
        preferences = UserPreference(
            id=uuid.uuid4(),
            user_id=user.id,
            theme="dark",
            llm_model="claude-3-sonnet",
            llm_temperature=0.7,
            llm_max_tokens=2000,
            notifications_enabled=True
        )
        db.add(preferences)
        db.flush()

        # Create test project
        project = Project(
            id=uuid.uuid4(),
            owner_id=user.id,
            name="AI Chat Bot",
            description="Build an AI chatbot with Socratic questioning",
            status="PLANNING",
            technology_stack=["Python", "FastAPI", "React"]
        )
        db.add(project)
        db.flush()

        # Create test session
        session = Session(
            id=uuid.uuid4(),
            owner_id=user.id,
            project_id=project.id,
            name="Initial Planning Session",
            status="ACTIVE",
            mode="chat",
            role="developer"
        )
        db.add(session)
        db.flush()

        # Create test messages
        user_message = Message(
            id=uuid.uuid4(),
            session_id=session.id,
            user_id=user.id,
            role="user",
            content="What are the key components of a Socratic questioning system?",
            message_type="text"
        )
        db.add(user_message)
        db.flush()

        assistant_message = Message(
            id=uuid.uuid4(),
            session_id=session.id,
            user_id=user.id,
            role="assistant",
            content="A Socratic questioning system should include: 1) User authentication, 2) Session management for maintaining context, 3) Question generation based on domain knowledge, 4) Real-time feedback, and 5) Progress tracking. Would you like to dive deeper into any of these components?",
            message_type="text"
        )
        db.add(assistant_message)

        db.commit()

        print("✅ Database seeded successfully!")
        print(f"  - Created user: testuser (test@example.com)")
        print(f"  - Created project: AI Chat Bot")
        print(f"  - Created session: Initial Planning Session")
        print(f"  - Created 2 test messages")
        print("\nLogin with:")
        print("  Username: testuser")
        print("  Password: Test@1234")

    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
