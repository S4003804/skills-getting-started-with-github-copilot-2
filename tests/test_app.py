from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_from_activity():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    initial_response = client.get("/activities")
    assert initial_response.status_code == 200
    assert email in initial_response.json()[activity_name]["participants"]

    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Removed {email} from {activity_name}"
    }

    updated_response = client.get("/activities")
    assert updated_response.status_code == 200
    assert email not in updated_response.json()[activity_name]["participants"]


def test_activities_response_is_not_cached():
    response = client.get("/activities")

    assert response.status_code == 200
    assert response.headers.get("cache-control") == "no-store"
