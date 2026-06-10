from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_root_redirects_to_static_index():
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_data():
    response = client.get("/activities")

    assert response.status_code == 200
    assert response.json()
    assert "Chess Club" in response.json()
    assert "Programming Class" in response.json()
    assert "Gym Class" in response.json()


def test_signup_for_activity_adds_participant():
    activity_name = "Chess Club"
    email = "test_student@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email in participants


def test_signup_for_unknown_activity_returns_404():
    response = client.post("/activities/UnknownClub/signup?email=test_student@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
