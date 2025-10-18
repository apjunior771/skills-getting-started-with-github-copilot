import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    # Make a shallow copy of participants for restoration after each test
    original = {k: v["participants"][:] for k, v in activities.items()}
    yield
    for k, lst in original.items():
        activities[k]["participants"] = lst[:]


def test_unregister_success():
    client = TestClient(app)
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Ensure email is present before unregistering
    assert email in activities[activity]["participants"]

    resp = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert resp.status_code == 200
    assert resp.json()["message"] == f"Unregistered {email} from {activity}"
    assert email not in activities[activity]["participants"]


def test_unregister_not_registered():
    client = TestClient(app)
    activity = "Chess Club"
    email = "not-registered@mergington.edu"

    assert email not in activities[activity]["participants"]

    resp = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert resp.status_code == 400
    assert "not registered" in resp.json().get("detail", "").lower()


def test_unregister_activity_not_found():
    client = TestClient(app)
    activity = "Nonexistent Club"
    email = "someone@mergington.edu"

    resp = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert resp.status_code == 404
