import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Fixture to provide a TestClient instance."""
    return TestClient(app)


class TestActivitiesAPI:
    """Integration tests for activities API endpoints."""

    def test_get_activities_success(self, client):
        """Test GET /activities returns all activities."""
        # Arrange - client fixture provides TestClient

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) > 0  # Should have activities
        # Check structure of first activity
        first_activity = next(iter(data.values()))
        assert "description" in first_activity
        assert "schedule" in first_activity
        assert "max_participants" in first_activity
        assert "participants" in first_activity

    def test_get_activities_includes_participant_count(self, client):
        """Test that GET /activities includes current participant count."""
        # Arrange
        activity_name = "Chess Club"

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert activity_name in data
        activity = data[activity_name]
        assert "participants" in activity
        assert isinstance(activity["participants"], list)

    def test_signup_success(self, client):
        """Test successful signup for an activity."""
        # Arrange
        activity_name = "Programming Class"
        email = "test@student.edu"

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]

    def test_signup_invalid_activity(self, client):
        """Test signup for non-existent activity returns 404."""
        # Arrange
        invalid_activity = "NonExistentActivity"
        email = "test@student.edu"

        # Act
        response = client.post(f"/activities/{invalid_activity}/signup?email={email}")

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data

    def test_signup_duplicate_email(self, client):
        """Test duplicate signup returns 400."""
        # Arrange
        activity_name = "Gym Class"
        email = "duplicate@student.edu"

        # First signup
        client.post(f"/activities/{activity_name}/signup?email={email}")

        # Act - Second signup with same email
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data

    def test_signup_missing_email(self, client):
        """Test signup without email parameter."""
        # Arrange
        activity_name = "Basketball Team"

        # Act
        response = client.post(f"/activities/{activity_name}/signup")

        # Assert
        assert response.status_code == 422  # Validation error

    def test_root_redirect(self, client):
        """Test root path redirects to static index."""
        # Arrange - no special setup

        # Act
        response = client.get("/")

        # Assert
        assert response.status_code == 200  # Redirect handled by FastAPI
        # Note: In test client, redirects are followed by default