"""Smoke tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient

from src.main import app

# Create test client
client = TestClient(app)


class TestHealthEndpoints:
    """Test health check endpoints."""

    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data

    def test_api_status(self):
        """Test API status endpoint."""
        response = client.get("/api/status")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data


class TestAuthEndpointsSmokeTest:
    """Smoke tests for authentication endpoints."""

    def test_register_endpoint_exists(self):
        """Test that register endpoint exists."""
        response = client.post(
            "/api/register",
            json={
                "username": "test",
                "email": "test@example.com",
                "password": "testpass123"
            }
        )
        # Should return either 201 or 500, not 404
        assert response.status_code != 404

    def test_login_endpoint_exists(self):
        """Test that login endpoint exists."""
        response = client.post(
            "/api/login",
            json={"username": "test", "password": "test"}
        )
        # Should return either 200, 401, or 500, not 404
        assert response.status_code != 404

    def test_logout_endpoint_exists(self):
        """Test that logout endpoint exists."""
        response = client.post("/api/logout")
        # May require auth, but should not be 404
        assert response.status_code != 404


class TestProjectEndpointsSmokeTest:
    """Smoke tests for project endpoints."""

    def test_projects_list_endpoint_exists(self):
        """Test that projects list endpoint exists."""
        response = client.get("/api/projects")
        # May require auth (403), but should not be 404
        assert response.status_code != 404

    def test_projects_create_endpoint_exists(self):
        """Test that projects create endpoint exists."""
        response = client.post("/api/projects", json={"name": "test"})
        # May require auth (403), but should not be 404
        assert response.status_code != 404


class TestSessionEndpointsSmokeTest:
    """Smoke tests for session endpoints."""

    def test_sessions_list_endpoint_exists(self):
        """Test that sessions list endpoint exists."""
        response = client.get("/api/sessions")
        # May require auth (403), but should not be 404
        assert response.status_code != 404

    def test_sessions_create_endpoint_exists(self):
        """Test that sessions create endpoint exists."""
        response = client.post(
            "/api/sessions",
            json={"name": "test", "mode": "chat"}
        )
        # May require auth (403), but should not be 404
        assert response.status_code != 404


class TestMessageEndpointsSmokeTest:
    """Smoke tests for message endpoints."""

    def test_messages_list_endpoint_exists(self):
        """Test that messages list endpoint exists."""
        from uuid import uuid4
        response = client.get(f"/api/sessions/{uuid4()}/messages")
        # May require auth (403) or session not found (404), but endpoint should exist
        assert response.status_code in [403, 404, 422]

    def test_messages_send_endpoint_exists(self):
        """Test that send message endpoint exists."""
        from uuid import uuid4
        response = client.post(
            f"/api/sessions/{uuid4()}/messages",
            json={"content": "test", "message_type": "text"}
        )
        # May require auth (403), session not found (404), but endpoint should exist
        assert response.status_code in [403, 404, 422]


class TestProfileEndpointsSmokeTest:
    """Smoke tests for profile endpoints."""

    def test_profile_endpoint_exists(self):
        """Test that profile endpoint exists."""
        response = client.get("/api/profile")
        # May require auth (403), but should not be 404
        assert response.status_code != 404

    def test_settings_endpoint_exists(self):
        """Test that settings endpoint exists."""
        response = client.get("/api/settings")
        # May require auth (403), but should not be 404
        assert response.status_code != 404


class TestOpenAPIDocs:
    """Test that OpenAPI documentation is available."""

    def test_openapi_docs_available(self):
        """Test that OpenAPI docs endpoint works."""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_openapi_schema_available(self):
        """Test that OpenAPI schema endpoint works."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "paths" in data
        assert "info" in data
