"""
Test suite for the Mergington High School Activities API
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app

# Create a test client
client = TestClient(app)


class TestBasicEndpoints:
    """Test basic API endpoints"""
    
    def test_root_redirect(self):
        """Test that root redirects to static/index.html"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"
    
    def test_get_activities(self):
        """Test getting all activities"""
        response = client.get("/activities")
        assert response.status_code == 200
        
        activities = response.json()
        assert isinstance(activities, dict)
        
        # Check that we have some activities
        assert len(activities) > 0
        
        # Check structure of each activity
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_name, str)
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)
            assert isinstance(activity_data["max_participants"], int)


class TestActivitySignup:
    """Test activity signup functionality"""
    
    def test_successful_signup(self):
        """Test successful student signup"""
        response = client.post(
            "/activities/Chess%20Club/signup",
            params={"email": "test@mergington.edu"}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "test@mergington.edu" in data["message"]
        assert "Chess Club" in data["message"]
    
    def test_signup_duplicate_student(self):
        """Test that duplicate signup is prevented"""
        email = "duplicate@mergington.edu"
        
        # First signup should succeed
        response1 = client.post(
            "/activities/Chess%20Club/signup",
            params={"email": email}
        )
        assert response1.status_code == 200
        
        # Second signup should fail
        response2 = client.post(
            "/activities/Chess%20Club/signup",
            params={"email": email}
        )
        assert response2.status_code == 400
        
        data = response2.json()
        assert "already signed up" in data["detail"].lower()
    
    def test_signup_nonexistent_activity(self):
        """Test signup for non-existent activity"""
        response = client.post(
            "/activities/Nonexistent%20Activity/signup",
            params={"email": "test@mergington.edu"}
        )
        assert response.status_code == 404
        
        data = response.json()
        assert "not found" in data["detail"].lower()
    
    def test_signup_activity_full(self):
        """Test signup when activity is at capacity"""
        # Get the Chess Club and fill it to capacity
        activities_response = client.get("/activities")
        activities = activities_response.json()
        chess_club = activities["Chess Club"]
        max_participants = chess_club["max_participants"]
        current_participants = len(chess_club["participants"])
        
        # Sign up students until we reach capacity
        spots_to_fill = max_participants - current_participants
        
        for i in range(spots_to_fill):
            email = f"student{i}@mergington.edu"
            response = client.post(
                "/activities/Chess%20Club/signup",
                params={"email": email}
            )
            # Should succeed until we hit capacity
            if i < spots_to_fill - 1:
                assert response.status_code in [200, 400]  # 400 if already exists
        
        # Now try to add one more - should fail
        response = client.post(
            "/activities/Chess%20Club/signup",
            params={"email": "overflow@mergington.edu"}
        )
        assert response.status_code == 400
        data = response.json()
        assert "full" in data["detail"].lower()


class TestActivityUnregister:
    """Test activity unregister functionality"""
    
    def test_successful_unregister(self):
        """Test successful student unregistration"""
        email = "unregister_test@mergington.edu"
        
        # First sign up
        signup_response = client.post(
            "/activities/Programming%20Class/signup",
            params={"email": email}
        )
        assert signup_response.status_code == 200
        
        # Then unregister
        unregister_response = client.delete(
            "/activities/Programming%20Class/unregister",
            params={"email": email}
        )
        assert unregister_response.status_code == 200
        
        data = unregister_response.json()
        assert "unregistered" in data["message"].lower()
        assert email in data["message"]
    
    def test_unregister_not_registered(self):
        """Test unregistering student who isn't registered"""
        response = client.delete(
            "/activities/Programming%20Class/unregister",
            params={"email": "notregistered@mergington.edu"}
        )
        assert response.status_code == 400
        
        data = response.json()
        assert "not registered" in data["detail"].lower()
    
    def test_unregister_nonexistent_activity(self):
        """Test unregistering from non-existent activity"""
        response = client.delete(
            "/activities/Nonexistent%20Activity/unregister",
            params={"email": "test@mergington.edu"}
        )
        assert response.status_code == 404
        
        data = response.json()
        assert "not found" in data["detail"].lower()


class TestDataIntegrity:
    """Test data integrity and edge cases"""
    
    def test_signup_and_unregister_cycle(self):
        """Test complete signup and unregister cycle"""
        email = "cycle_test@mergington.edu"
        activity = "Art%20Club"
        
        # Get initial participant count
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()["Art Club"]["participants"])
        
        # Sign up
        signup_response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert signup_response.status_code == 200
        
        # Verify participant was added
        after_signup_response = client.get("/activities")
        after_signup_count = len(after_signup_response.json()["Art Club"]["participants"])
        assert after_signup_count == initial_count + 1
        
        # Unregister
        unregister_response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        assert unregister_response.status_code == 200
        
        # Verify participant was removed
        after_unregister_response = client.get("/activities")
        after_unregister_count = len(after_unregister_response.json()["Art Club"]["participants"])
        assert after_unregister_count == initial_count
    
    def test_email_validation_characters(self):
        """Test signup with various email formats"""
        valid_emails = [
            "student@mergington.edu",
            "first.last@mergington.edu",
            "student123@mergington.edu",
            "student+tag@mergington.edu"
        ]
        
        for email in valid_emails:
            response = client.post(
                "/activities/Drama%20Club/signup",
                params={"email": email}
            )
            # Should either succeed or fail due to duplicate, not format
            assert response.status_code in [200, 400]
    
    def test_activity_names_with_spaces(self):
        """Test that activities with spaces in names work correctly"""
        response = client.post(
            "/activities/Math%20Olympiad/signup",
            params={"email": "mathstudent@mergington.edu"}
        )
        assert response.status_code in [200, 400]  # 400 if already registered
    
    def test_concurrent_signups(self):
        """Test multiple signups for different activities by same student"""
        email = "multisport@mergington.edu"
        
        activities = ["Soccer%20Club", "Basketball%20Team"]
        
        for activity in activities:
            response = client.post(
                f"/activities/{activity}/signup",
                params={"email": email}
            )
            assert response.status_code in [200, 400]  # 400 if already exists or full


class TestAPIDocumentation:
    """Test API metadata and documentation"""
    
    def test_openapi_schema(self):
        """Test that OpenAPI schema is available"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert "paths" in schema


if __name__ == "__main__":
    pytest.main([__file__])