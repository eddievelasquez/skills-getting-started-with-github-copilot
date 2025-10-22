"""
Pytest configuration and fixtures for the Mergington High School API tests
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
import copy


@pytest.fixture(scope="function")
def client():
    """Create a test client for each test function"""
    return TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def reset_activities_data():
    """Reset activities data before each test to ensure clean state"""
    # Store original activities data
    original_activities = copy.deepcopy(activities)
    
    # Reset to original state before each test
    activities.clear()
    activities.update({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Soccer Club": {
            "description": "Outdoor soccer practice and interschool matches",
            "schedule": "Wednesdays and Saturdays, 4:00 PM - 6:00 PM",
            "max_participants": 22,
            "participants": ["liam@mergington.edu", "noah@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball team training and games",
            "schedule": "Mondays, Thursdays, 5:00 PM - 7:00 PM",
            "max_participants": 15,
            "participants": ["ava@mergington.edu", "isabella@mergington.edu"]
        },
        "Art Club": {
            "description": "Explore painting, drawing, and mixed media projects",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["mia@mergington.edu", "charlotte@mergington.edu"]
        },
        "Drama Club": {
            "description": "Acting, stagecraft, and school productions",
            "schedule": "Fridays, 4:00 PM - 6:00 PM",
            "max_participants": 25,
            "participants": ["henry@mergington.edu", "grace@mergington.edu"]
        },
        "Math Olympiad": {
            "description": "Advanced problem solving and competition preparation",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["lucas@mergington.edu", "elijah@mergington.edu"]
        },
        "Science Club": {
            "description": "Hands-on experiments, projects, and science fairs",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
        }
    })
    
    yield
    
    # Restore original state after each test
    activities.clear()
    activities.update(original_activities)


@pytest.fixture
def sample_activities():
    """Fixture providing sample activities data for testing"""
    return {
        "Test Activity": {
            "description": "A test activity for unit testing",
            "schedule": "Test Schedule",
            "max_participants": 5,
            "participants": ["test1@mergington.edu", "test2@mergington.edu"]
        }
    }


@pytest.fixture
def valid_student_email():
    """Fixture providing a valid student email for testing"""
    return "teststudent@mergington.edu"


@pytest.fixture
def invalid_student_email():
    """Fixture providing an invalid student email for testing"""
    return "invalid-email-format"