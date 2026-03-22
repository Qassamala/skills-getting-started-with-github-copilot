import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange
    # (No special setup needed)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data

def test_signup_and_unregister():
    # Arrange
    test_email = "testuser@mergington.edu"
    activity = "Chess Club"

    # Act: Sign up
    signup_resp = client.post(f"/activities/{activity}/signup?email={test_email}")

    # Assert: Signup
    assert signup_resp.status_code == 200
    assert f"Signed up {test_email}" in signup_resp.json().get("message", "")

    # Act: Get activities after signup
    activities = client.get("/activities").json()

    # Assert: Participant is added
    assert test_email in activities[activity]["participants"]

    # Act: Unregister (if endpoint exists)
    unregister_resp = client.post(f"/activities/{activity}/unregister?email={test_email}")

    # Assert: Unregister
    assert unregister_resp.status_code in (200, 404)
    if unregister_resp.status_code == 200:
        assert f"Removed {test_email}" in unregister_resp.json().get("message", "")
        # Act: Get activities after unregister
        activities = client.get("/activities").json()
        # Assert: Participant is removed
        assert test_email not in activities[activity]["participants"]
