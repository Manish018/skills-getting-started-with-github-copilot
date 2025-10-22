import pytest
from fastapi.testclient import TestClient
from src.app import app

@pytest.fixture
def client():
    """Create a test client for the FastAPI application"""
    return TestClient(app)

@pytest.fixture
def test_activity():
    """Sample activity data for testing"""
    return {
        "Test Club": {
            "description": "A test activity for unit testing",
            "schedule": "Test Schedule",
            "max_participants": 5,
            "participants": ["test@mergington.edu"]
        }
    }