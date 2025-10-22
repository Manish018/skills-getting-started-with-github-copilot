from fastapi.testclient import TestClient
import pytest

def test_root_redirect(client: TestClient):
    """Test that the root endpoint redirects to static/index.html"""
    response = client.get("/")
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"

def test_get_activities(client: TestClient):
    """Test getting the list of activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) > 0
    
    # Check activity structure
    for name, details in activities.items():
        assert isinstance(name, str)
        assert isinstance(details, dict)
        assert "description" in details
        assert "schedule" in details
        assert "max_participants" in details
        assert "participants" in details
        assert isinstance(details["participants"], list)

def test_signup_for_activity(client: TestClient):
    """Test signing up for an activity"""
    # First get available activities
    response = client.get("/activities")
    activities = response.json()
    activity_name = list(activities.keys())[0]
    
    # Try to sign up a new participant
    email = "newstudent@mergington.edu"
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert email in result["message"]
    assert activity_name in result["message"]

    # Verify participant was added
    response = client.get("/activities")
    activities = response.json()
    assert email in activities[activity_name]["participants"]

def test_signup_duplicate(client: TestClient):
    """Test that a student cannot sign up for the same activity twice"""
    # First get available activities
    response = client.get("/activities")
    activities = response.json()
    activity_name = list(activities.keys())[0]
    
    # Sign up a participant
    email = "duplicate@mergington.edu"
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    
    # Try to sign up the same participant again
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_nonexistent_activity(client: TestClient):
    """Test signing up for a non-existent activity"""
    response = client.post("/activities/NonExistentClub/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_unregister_from_activity(client: TestClient):
    """Test unregistering from an activity"""
    # First get available activities
    response = client.get("/activities")
    activities = response.json()
    activity_name = list(activities.keys())[0]
    
    # Sign up a participant first
    email = "tounregister@mergington.edu"
    client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Now unregister them
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert email in result["message"]
    assert activity_name in result["message"]

    # Verify participant was removed
    response = client.get("/activities")
    activities = response.json()
    assert email not in activities[activity_name]["participants"]

def test_unregister_not_registered(client: TestClient):
    """Test unregistering a participant who isn't registered"""
    # First get available activities
    response = client.get("/activities")
    activities = response.json()
    activity_name = list(activities.keys())[0]
    
    # Try to unregister a participant who isn't registered
    email = "notregistered@mergington.edu"
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]