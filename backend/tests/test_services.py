"""Comprehensive unit tests for service layer."""

import pytest
from uuid import uuid4
from datetime import datetime, timedelta

from backend.src.services.user_service import UserService
from backend.src.services.project_service import ProjectService
from backend.src.services.session_service import SessionService
from backend.src.services.message_service import MessageService
from backend.src.services.preference_service import PreferenceService
from backend.src.repositories import (
    UserRepository,
    ProjectRepository,
    SessionRepository,
    MessageRepository,
    PreferenceRepository,
)
from backend.src.models import User, Project, Session, Message, UserPreference


class TestUserService:
    """Test UserService functionality."""

    def test_register_user_success(self, db):
        """Test successful user registration."""
        service = UserService(db)

        user = service.register_user(
            username="testuser",
            email="test@example.com",
            password="SecurePass123",
            first_name="John",
            last_name="Doe",
        )

        assert user is not None
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.hashed_password != "SecurePass123"  # Should be hashed
        assert user.status == "ACTIVE"

    def test_register_duplicate_username(self, db):
        """Test registering with duplicate username."""
        service = UserService(db)

        # Create first user
        service.register_user(
            username="testuser",
            email="test1@example.com",
            password="Password123",
        )

        # Try to create duplicate
        with pytest.raises(ValueError, match="Username already exists"):
            service.register_user(
                username="testuser",
                email="test2@example.com",
                password="Password123",
            )

    def test_register_duplicate_email(self, db):
        """Test registering with duplicate email."""
        service = UserService(db)

        # Create first user
        service.register_user(
            username="user1",
            email="test@example.com",
            password="Password123",
        )

        # Try to create duplicate
        with pytest.raises(ValueError, match="Email already exists"):
            service.register_user(
                username="user2",
                email="test@example.com",
                password="Password123",
            )

    def test_authenticate_user_success(self, db):
        """Test successful authentication."""
        service = UserService(db)

        # Create user
        created_user = service.register_user(
            username="testuser",
            email="test@example.com",
            password="SecurePass123",
        )

        # Authenticate
        auth_user = service.authenticate_user("testuser", "SecurePass123")

        assert auth_user is not None
        assert auth_user.id == created_user.id
        assert auth_user.username == "testuser"

    def test_authenticate_wrong_password(self, db):
        """Test authentication with wrong password."""
        service = UserService(db)

        service.register_user(
            username="testuser",
            email="test@example.com",
            password="SecurePass123",
        )

        auth_user = service.authenticate_user("testuser", "wrongpassword")
        assert auth_user is None

    def test_authenticate_nonexistent_user(self, db):
        """Test authentication for nonexistent user."""
        service = UserService(db)

        auth_user = service.authenticate_user("nonexistent", "Password123")
        assert auth_user is None

    def test_password_hashing(self, db):
        """Test that passwords are properly hashed."""
        service = UserService(db)

        password = "mypassword123"
        hashed = service.hash_password(password)

        assert hashed != password
        assert service.verify_password(password, hashed)
        assert not service.verify_password("wrongpassword", hashed)

    def test_update_profile(self, db):
        """Test updating user profile."""
        service = UserService(db)

        user = service.register_user(
            username="testuser",
            email="test@example.com",
            password="Password123",
        )

        user.first_name = "Jane"
        user.last_name = "Smith"
        user.bio = "Software Engineer"
        db.commit()

        updated_user = db.query(User).filter_by(id=user.id).first()
        assert updated_user.first_name == "Jane"
        assert updated_user.last_name == "Smith"
        assert updated_user.bio == "Software Engineer"


class TestProjectService:
    """Test ProjectService functionality."""

    def test_create_project(self, db, test_user):
        """Test creating a project."""
        service = ProjectService(db)

        project = service.create_project(
            name="My Project",
            description="Test project",
            owner_id=test_user.id,
            technology_stack=["Python", "FastAPI"],
        )

        assert project is not None
        assert project.name == "My Project"
        assert project.description == "Test project"
        assert project.owner_id == test_user.id
        assert project.status == "ACTIVE"
        assert project.technology_stack == ["Python", "FastAPI"]

    def test_get_project_by_id(self, db, test_user):
        """Test retrieving project by ID."""
        service = ProjectService(db)

        created = service.create_project(
            name="Test Project",
            owner_id=test_user.id,
        )

        retrieved = service.get_project_by_id(created.id)
        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.name == "Test Project"

    def test_get_nonexistent_project(self, db):
        """Test retrieving nonexistent project."""
        service = ProjectService(db)

        project = service.get_project_by_id(uuid4())
        assert project is None

    def test_delete_project(self, db, test_user):
        """Test deleting a project."""
        service = ProjectService(db)

        project = service.create_project(
            name="Test Project",
            owner_id=test_user.id,
        )

        service.delete_project(project.id)
        db.commit()

        retrieved = service.get_project_by_id(project.id)
        assert retrieved is None


class TestSessionService:
    """Test SessionService functionality."""

    def test_create_session(self, db, test_user, test_project):
        """Test creating a session."""
        service = SessionService(db)

        session = service.create_session(
            name="Learning Session",
            mode="chat",
            owner_id=test_user.id,
            project_id=test_project.id,
        )

        assert session is not None
        assert session.name == "Learning Session"
        assert session.mode == "chat"
        assert session.owner_id == test_user.id
        assert session.status == "ACTIVE"

    def test_create_session_invalid_mode(self, db, test_user):
        """Test creating session with invalid mode."""
        service = SessionService(db)

        with pytest.raises(ValueError):
            service.create_session(
                name="Test",
                mode="invalid_mode",
                owner_id=test_user.id,
            )

    def test_get_session_by_id(self, db, test_user, test_project):
        """Test retrieving session."""
        service = SessionService(db)

        created = service.create_session(
            name="Test Session",
            mode="chat",
            owner_id=test_user.id,
            project_id=test_project.id,
        )

        retrieved = service.get_session_by_id(created.id)
        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.name == "Test Session"

    def test_delete_session(self, db, test_user, test_project):
        """Test deleting a session."""
        service = SessionService(db)

        session = service.create_session(
            name="Test Session",
            mode="chat",
            owner_id=test_user.id,
            project_id=test_project.id,
        )

        service.delete_session(session.id)
        db.commit()

        retrieved = service.get_session_by_id(session.id)
        assert retrieved is None


class TestMessageService:
    """Test MessageService functionality."""

    def test_create_message(self, db, test_user, test_session):
        """Test creating a message."""
        service = MessageService(db)

        message = service.create_message(
            session_id=test_session.id,
            user_id=test_user.id,
            content="Hello, World!",
            role="user",
            message_type="text",
        )

        assert message is not None
        assert message.content == "Hello, World!"
        assert message.role == "user"
        assert message.session_id == test_session.id

    def test_get_messages_by_session(self, db, test_user, test_session):
        """Test retrieving messages from a session."""
        service = MessageService(db)

        # Create multiple messages
        for i in range(3):
            service.create_message(
                session_id=test_session.id,
                user_id=test_user.id,
                content=f"Message {i}",
                role="user",
                message_type="text",
            )

        messages = service.get_messages_by_session(test_session.id)
        assert len(messages) == 3

    def test_count_messages(self, db, test_user, test_session):
        """Test counting messages in a session."""
        service = MessageService(db)

        for i in range(5):
            service.create_message(
                session_id=test_session.id,
                user_id=test_user.id,
                content=f"Message {i}",
                role="user",
                message_type="text",
            )

        count = service.count_messages(session_id=test_session.id)
        assert count == 5


class TestPreferenceService:
    """Test PreferenceService functionality."""

    def test_create_default_preferences(self, db, test_user):
        """Test creating default preferences."""
        service = PreferenceService(db)

        prefs = service.create_default_preferences(test_user.id)

        assert prefs is not None
        assert prefs.user_id == test_user.id
        assert prefs.theme == "light"
        assert prefs.llm_model == "claude-3-5-sonnet-20241022"
        assert prefs.llm_temperature == 0.7
        assert prefs.auto_sync is True
        assert prefs.notifications_enabled is True

    def test_get_preferences(self, db, test_user):
        """Test retrieving user preferences."""
        service = PreferenceService(db)

        created = service.create_default_preferences(test_user.id)
        db.commit()

        retrieved = service.get_preferences(test_user.id)
        assert retrieved is not None
        assert retrieved.id == created.id

    def test_update_preferences(self, db, test_user):
        """Test updating preferences."""
        service = PreferenceService(db)

        prefs = service.create_default_preferences(test_user.id)
        db.commit()

        prefs.theme = "dark"
        prefs.llm_temperature = 0.9
        db.commit()

        updated = service.get_preferences(test_user.id)
        assert updated.theme == "dark"
        assert updated.llm_temperature == 0.9


class TestServiceIntegration:
    """Integration tests for multiple services working together."""

    def test_user_project_session_flow(self, db):
        """Test complete flow: create user, project, and session."""
        # Create user
        user_service = UserService(db)
        user = user_service.register_user(
            username="testuser",
            email="test@example.com",
            password="Password123",
        )
        db.commit()

        # Create project
        project_service = ProjectService(db)
        project = project_service.create_project(
            name="Test Project",
            owner_id=user.id,
        )
        db.commit()

        # Create session
        session_service = SessionService(db)
        session = session_service.create_session(
            name="Test Session",
            mode="chat",
            owner_id=user.id,
            project_id=project.id,
        )
        db.commit()

        # Create message
        message_service = MessageService(db)
        message = message_service.create_message(
            session_id=session.id,
            user_id=user.id,
            content="Hello!",
            role="user",
            message_type="text",
        )
        db.commit()

        # Verify all relationships
        assert user.id is not None
        assert project.owner_id == user.id
        assert session.owner_id == user.id
        assert session.project_id == project.id
        assert message.session_id == session.id
        assert message.user_id == user.id

    def test_end_to_end_workflow(self, db):
        """Test complete end-to-end workflow."""
        # Register user
        user_service = UserService(db)
        user = user_service.register_user(
            username="learner",
            email="learner@example.com",
            password="Secure123",
            first_name="John",
            last_name="Learner",
        )
        db.commit()

        # Authenticate user
        auth_user = user_service.authenticate_user("learner", "Secure123")
        assert auth_user is not None

        # Create project
        project_service = ProjectService(db)
        project = project_service.create_project(
            name="Python Learning",
            description="Learn Python basics",
            owner_id=user.id,
            technology_stack=["Python"],
        )
        db.commit()

        # Create session
        session_service = SessionService(db)
        session = session_service.create_session(
            name="Variables and Types",
            mode="teaching",
            owner_id=user.id,
            project_id=project.id,
        )
        db.commit()

        # Add messages
        message_service = MessageService(db)
        message_service.create_message(
            session_id=session.id,
            user_id=user.id,
            content="What is a variable?",
            role="user",
            message_type="question",
        )
        db.commit()

        # Set preferences
        pref_service = PreferenceService(db)
        prefs = pref_service.create_default_preferences(user.id)
        prefs.theme = "dark"
        prefs.llm_temperature = 0.5
        db.commit()

        # Verify complete workflow
        assert auth_user.username == "learner"
        assert project.name == "Python Learning"
        assert session.mode == "teaching"
        messages = message_service.get_messages_by_session(session.id)
        assert len(messages) == 1
        assert prefs.theme == "dark"
