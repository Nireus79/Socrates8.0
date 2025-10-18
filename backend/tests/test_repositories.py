"""Tests for repository layer."""

import uuid
import pytest
from passlib.context import CryptContext

from backend.src.repositories import (
    UserRepository,
    ProjectRepository,
    SessionRepository,
    MessageRepository,
    PreferenceRepository,
    DocumentRepository,
    AuditLogRepository,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TestUserRepository:
    """Tests for UserRepository."""

    def test_create_user(self, db):
        """Test creating a user."""
        repo = UserRepository(db)
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password_hash": pwd_context.hash("Test@1234"),
            "first_name": "Test",
            "last_name": "User",
        }
        user = repo.create(user_data)
        db.commit()

        assert user.username == "testuser"
        assert user.email == "test@example.com"

    def test_get_by_username(self, db):
        """Test getting user by username."""
        repo = UserRepository(db)
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password_hash": pwd_context.hash("Test@1234"),
        }
        repo.create(user_data)
        db.commit()

        user = repo.get_by_username("testuser")
        assert user is not None
        assert user.username == "testuser"

    def test_get_by_email(self, db):
        """Test getting user by email."""
        repo = UserRepository(db)
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password_hash": pwd_context.hash("Test@1234"),
        }
        repo.create(user_data)
        db.commit()

        user = repo.get_by_email("test@example.com")
        assert user is not None
        assert user.email == "test@example.com"

    def test_get_by_id(self, db):
        """Test getting user by ID."""
        repo = UserRepository(db)
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password_hash": pwd_context.hash("Test@1234"),
        }
        user = repo.create(user_data)
        db.commit()

        retrieved = repo.get_by_id(user.id)
        assert retrieved is not None
        assert retrieved.id == user.id

    def test_update_user(self, db):
        """Test updating a user."""
        repo = UserRepository(db)
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password_hash": pwd_context.hash("Test@1234"),
        }
        user = repo.create(user_data)
        db.commit()

        updated = repo.update(user.id, {"first_name": "Updated"})
        db.commit()

        assert updated.first_name == "Updated"

    def test_delete_user(self, db):
        """Test deleting a user."""
        repo = UserRepository(db)
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password_hash": pwd_context.hash("Test@1234"),
        }
        user = repo.create(user_data)
        db.commit()

        result = repo.delete(user.id)
        db.commit()

        assert result is True
        assert repo.get_by_id(user.id) is None

    def test_count_users(self, db):
        """Test counting users."""
        repo = UserRepository(db)
        repo.create({
            "username": "user1",
            "email": "user1@example.com",
            "password_hash": "hash1",
        })
        repo.create({
            "username": "user2",
            "email": "user2@example.com",
            "password_hash": "hash2",
        })
        db.commit()

        count = repo.count()
        assert count == 2


class TestProjectRepository:
    """Tests for ProjectRepository."""

    @pytest.fixture
    def user(self, db):
        """Create test user."""
        repo = UserRepository(db)
        user = repo.create({
            "username": "testuser",
            "email": "test@example.com",
            "password_hash": pwd_context.hash("Test@1234"),
        })
        db.commit()
        return user

    def test_create_project(self, db, user):
        """Test creating a project."""
        repo = ProjectRepository(db)
        project = repo.create({
            "owner_id": user.id,
            "name": "Test Project",
            "description": "Test description",
            "status": "PLANNING",
        })
        db.commit()

        assert project.name == "Test Project"
        assert project.owner_id == user.id

    def test_get_by_owner(self, db, user):
        """Test getting projects by owner."""
        repo = ProjectRepository(db)
        repo.create({
            "owner_id": user.id,
            "name": "Project 1",
            "status": "PLANNING",
        })
        repo.create({
            "owner_id": user.id,
            "name": "Project 2",
            "status": "DEVELOPMENT",
        })
        db.commit()

        projects = repo.get_by_owner(user.id)
        assert len(projects) == 2

    def test_get_by_status(self, db, user):
        """Test getting projects by status."""
        repo = ProjectRepository(db)
        repo.create({
            "owner_id": user.id,
            "name": "Project 1",
            "status": "PLANNING",
        })
        repo.create({
            "owner_id": user.id,
            "name": "Project 2",
            "status": "DEVELOPMENT",
        })
        db.commit()

        projects = repo.get_by_status("PLANNING")
        assert len(projects) == 1


class TestSessionRepository:
    """Tests for SessionRepository."""

    @pytest.fixture
    def user_and_project(self, db):
        """Create test user and project."""
        user_repo = UserRepository(db)
        user = user_repo.create({
            "username": "testuser",
            "email": "test@example.com",
            "password_hash": pwd_context.hash("Test@1234"),
        })

        project_repo = ProjectRepository(db)
        project = project_repo.create({
            "owner_id": user.id,
            "name": "Test Project",
            "status": "PLANNING",
        })
        db.commit()
        return user, project

    def test_create_session(self, db, user_and_project):
        """Test creating a session."""
        user, project = user_and_project
        repo = SessionRepository(db)
        session = repo.create({
            "owner_id": user.id,
            "project_id": project.id,
            "name": "Test Session",
            "status": "ACTIVE",
            "mode": "chat",
        })
        db.commit()

        assert session.name == "Test Session"
        assert session.mode == "chat"

    def test_get_by_owner(self, db, user_and_project):
        """Test getting sessions by owner."""
        user, project = user_and_project
        repo = SessionRepository(db)
        repo.create({
            "owner_id": user.id,
            "project_id": project.id,
            "name": "Session 1",
            "status": "ACTIVE",
            "mode": "chat",
        })
        repo.create({
            "owner_id": user.id,
            "project_id": project.id,
            "name": "Session 2",
            "status": "ACTIVE",
            "mode": "question",
        })
        db.commit()

        sessions = repo.get_by_owner(user.id)
        assert len(sessions) == 2

    def test_get_active_sessions(self, db, user_and_project):
        """Test getting active sessions."""
        user, project = user_and_project
        repo = SessionRepository(db)
        repo.create({
            "owner_id": user.id,
            "project_id": project.id,
            "name": "Active Session",
            "status": "ACTIVE",
            "mode": "chat",
        })
        repo.create({
            "owner_id": user.id,
            "project_id": project.id,
            "name": "Archived Session",
            "status": "ARCHIVED",
            "mode": "chat",
        })
        db.commit()

        active = repo.get_active_sessions(user.id)
        assert len(active) == 1
        assert active[0].name == "Active Session"


class TestMessageRepository:
    """Tests for MessageRepository."""

    @pytest.fixture
    def user_project_session(self, db):
        """Create test user, project, and session."""
        user_repo = UserRepository(db)
        user = user_repo.create({
            "username": "testuser",
            "email": "test@example.com",
            "password_hash": pwd_context.hash("Test@1234"),
        })

        project_repo = ProjectRepository(db)
        project = project_repo.create({
            "owner_id": user.id,
            "name": "Test Project",
            "status": "PLANNING",
        })

        session_repo = SessionRepository(db)
        session = session_repo.create({
            "owner_id": user.id,
            "project_id": project.id,
            "name": "Test Session",
            "status": "ACTIVE",
            "mode": "chat",
        })
        db.commit()
        return user, project, session

    def test_create_message(self, db, user_project_session):
        """Test creating a message."""
        user, project, session = user_project_session
        repo = MessageRepository(db)
        message = repo.create({
            "session_id": session.id,
            "user_id": user.id,
            "role": "user",
            "content": "Test message",
            "message_type": "text",
        })
        db.commit()

        assert message.content == "Test message"
        assert message.role == "user"

    def test_get_by_session(self, db, user_project_session):
        """Test getting messages by session."""
        user, project, session = user_project_session
        repo = MessageRepository(db)
        repo.create({
            "session_id": session.id,
            "user_id": user.id,
            "role": "user",
            "content": "Message 1",
            "message_type": "text",
        })
        repo.create({
            "session_id": session.id,
            "user_id": user.id,
            "role": "assistant",
            "content": "Response 1",
            "message_type": "text",
        })
        db.commit()

        messages = repo.get_by_session(session.id)
        assert len(messages) == 2

    def test_get_by_role(self, db, user_project_session):
        """Test getting messages by role."""
        user, project, session = user_project_session
        repo = MessageRepository(db)
        repo.create({
            "session_id": session.id,
            "user_id": user.id,
            "role": "user",
            "content": "User message",
            "message_type": "text",
        })
        repo.create({
            "session_id": session.id,
            "user_id": user.id,
            "role": "assistant",
            "content": "Assistant message",
            "message_type": "text",
        })
        db.commit()

        assistant_messages = repo.get_by_role(session.id, "assistant")
        assert len(assistant_messages) == 1
        assert assistant_messages[0].role == "assistant"

    def test_get_session_count(self, db, user_project_session):
        """Test getting message count."""
        user, project, session = user_project_session
        repo = MessageRepository(db)
        repo.create({
            "session_id": session.id,
            "user_id": user.id,
            "role": "user",
            "content": "Message 1",
            "message_type": "text",
        })
        repo.create({
            "session_id": session.id,
            "user_id": user.id,
            "role": "assistant",
            "content": "Message 2",
            "message_type": "text",
        })
        db.commit()

        count = repo.get_by_session_count(session.id)
        assert count == 2


class TestPreferenceRepository:
    """Tests for PreferenceRepository."""

    @pytest.fixture
    def user(self, db):
        """Create test user."""
        repo = UserRepository(db)
        user = repo.create({
            "username": "testuser",
            "email": "test@example.com",
            "password_hash": pwd_context.hash("Test@1234"),
        })
        db.commit()
        return user

    def test_create_preference(self, db, user):
        """Test creating preferences."""
        repo = PreferenceRepository(db)
        prefs = repo.create({
            "user_id": user.id,
            "theme": "dark",
            "llm_model": "claude-3-sonnet",
        })
        db.commit()

        assert prefs.theme == "dark"
        assert prefs.llm_model == "claude-3-sonnet"

    def test_get_by_user_id(self, db, user):
        """Test getting preferences by user ID."""
        repo = PreferenceRepository(db)
        repo.create({
            "user_id": user.id,
            "theme": "light",
        })
        db.commit()

        prefs = repo.get_by_user_id(user.id)
        assert prefs is not None
        assert prefs.theme == "light"

    def test_create_for_user(self, db, user):
        """Test creating default preferences for user."""
        repo = PreferenceRepository(db)
        prefs = repo.create_for_user(user.id)
        db.commit()

        assert prefs.user_id == user.id
        assert prefs.theme == "dark"  # default


class TestDocumentRepository:
    """Tests for DocumentRepository."""

    @pytest.fixture
    def user_and_project(self, db):
        """Create test user and project."""
        user_repo = UserRepository(db)
        user = user_repo.create({
            "username": "testuser",
            "email": "test@example.com",
            "password_hash": pwd_context.hash("Test@1234"),
        })

        project_repo = ProjectRepository(db)
        project = project_repo.create({
            "owner_id": user.id,
            "name": "Test Project",
            "status": "PLANNING",
        })
        db.commit()
        return user, project

    def test_create_document(self, db, user_and_project):
        """Test creating a document."""
        user, project = user_and_project
        repo = DocumentRepository(db)
        doc = repo.create({
            "owner_id": user.id,
            "project_id": project.id,
            "filename": "test.pdf",
            "file_path": "/uploads/test.pdf",
            "file_type": "pdf",
            "status": "PROCESSED",
        })
        db.commit()

        assert doc.filename == "test.pdf"
        assert doc.status == "PROCESSED"

    def test_get_by_owner(self, db, user_and_project):
        """Test getting documents by owner."""
        user, project = user_and_project
        repo = DocumentRepository(db)
        repo.create({
            "owner_id": user.id,
            "project_id": project.id,
            "filename": "doc1.pdf",
            "file_path": "/uploads/doc1.pdf",
        })
        repo.create({
            "owner_id": user.id,
            "project_id": project.id,
            "filename": "doc2.docx",
            "file_path": "/uploads/doc2.docx",
        })
        db.commit()

        docs = repo.get_by_owner(user.id)
        assert len(docs) == 2


class TestAuditLogRepository:
    """Tests for AuditLogRepository."""

    @pytest.fixture
    def user(self, db):
        """Create test user."""
        repo = UserRepository(db)
        user = repo.create({
            "username": "testuser",
            "email": "test@example.com",
            "password_hash": pwd_context.hash("Test@1234"),
        })
        db.commit()
        return user

    def test_create_audit_log(self, db, user):
        """Test creating an audit log."""
        repo = AuditLogRepository(db)
        log = repo.create({
            "user_id": user.id,
            "entity_type": "User",
            "entity_id": user.id,
            "action": "CREATE",
            "new_value": {"username": "testuser"},
        })
        db.commit()

        assert log.action == "CREATE"
        assert log.entity_type == "User"

    def test_get_by_user(self, db, user):
        """Test getting audit logs by user."""
        repo = AuditLogRepository(db)
        repo.create({
            "user_id": user.id,
            "entity_type": "User",
            "entity_id": user.id,
            "action": "UPDATE",
        })
        repo.create({
            "user_id": user.id,
            "entity_type": "Project",
            "entity_id": uuid.uuid4(),
            "action": "CREATE",
        })
        db.commit()

        logs = repo.get_by_user(user.id)
        assert len(logs) == 2

    def test_get_by_action(self, db, user):
        """Test getting audit logs by action."""
        repo = AuditLogRepository(db)
        repo.create({
            "user_id": user.id,
            "entity_type": "User",
            "entity_id": user.id,
            "action": "CREATE",
        })
        repo.create({
            "user_id": user.id,
            "entity_type": "User",
            "entity_id": user.id,
            "action": "UPDATE",
        })
        db.commit()

        creates = repo.get_by_action("CREATE")
        assert len(creates) == 1
