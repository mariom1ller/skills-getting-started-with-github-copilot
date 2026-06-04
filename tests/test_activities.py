from src.app import activities


def test_root_redirects(client):
    # Arrange
    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code in (302, 307)
    assert response.headers["location"] == "/static/index.html"


def test_get_activities(client):
    # Arrange
    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_for_activity(client):
    # Arrange
    activity = "Chess Club"
    email = "testuser@example.com"
    # Ensure email is not present before test
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email in activities[activity]["participants"]
    assert response.json()["message"] == f"Signed up {email} for {activity}"

    # Cleanup
    activities[activity]["participants"].remove(email)


def test_signup_duplicate_fails(client):
    # Arrange
    activity = "Chess Club"
    email = "duplicate@example.com"
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)
    activities[activity]["participants"].append(email)

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

    # Cleanup
    activities[activity]["participants"].remove(email)


def test_unregister_participant(client):
    # Arrange
    activity = "Programming Class"
    email = "removeme@example.com"
    if email not in activities[activity]["participants"]:
        activities[activity]["participants"].append(email)

    # Act
    response = client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email not in activities[activity]["participants"]

    # Act: try removing again -> should 404
    response2 = client.delete(f"/activities/{activity}/participants", params={"email": email})
    assert response2.status_code == 404
