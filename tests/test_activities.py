def test_root_redirect(client):
    """Test that root endpoint redirects to static index.html"""
    # Arrange
    expected_url = "/static/index.html"
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307
    assert expected_url in response.headers["location"]


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all activities with correct structure"""
    # Arrange
    expected_activities = ["Chess Club", "Programming Class", "Gym Class"]
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert response.status_code == 200
    assert len(activities) == 3
    for activity_name in expected_activities:
        assert activity_name in activities
        assert "description" in activities[activity_name]
        assert "schedule" in activities[activity_name]
        assert "max_participants" in activities[activity_name]
        assert "participants" in activities[activity_name]


def test_get_activities_contains_participants(client):
    """Test that activity participants are correctly listed"""
    # Arrange
    expected_participant = "michael@mergington.edu"
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert response.status_code == 200
    assert expected_participant in activities["Chess Club"]["participants"]


def test_signup_for_activity_success(client):
    """Test successful signup for an activity"""
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    initial_count = len(client.get("/activities").json()[activity_name]["participants"])
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    
    # Verify participant was added
    updated_activities = client.get("/activities").json()
    updated_count = len(updated_activities[activity_name]["participants"])
    assert updated_count == initial_count + 1
    assert email in updated_activities[activity_name]["participants"]


def test_signup_duplicate_participant_fails(client):
    """Test that signing up twice for the same activity fails"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_nonexistent_activity_fails(client):
    """Test that signup for non-existent activity returns 404"""
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "test@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_participant_success(client):
    """Test successful unregistration of a participant"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already registered
    initial_count = len(client.get("/activities").json()[activity_name]["participants"])
    
    # Act
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    
    # Assert
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]
    
    # Verify participant was removed
    updated_activities = client.get("/activities").json()
    updated_count = len(updated_activities[activity_name]["participants"])
    assert updated_count == initial_count - 1
    assert email not in updated_activities[activity_name]["participants"]


def test_unregister_nonexistent_participant_fails(client):
    """Test that unregistering a non-existent participant fails"""
    # Arrange
    activity_name = "Chess Club"
    email = "notregistered@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    
    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]


def test_unregister_nonexistent_activity_fails(client):
    """Test that unregister for non-existent activity returns 404"""
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "test@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
