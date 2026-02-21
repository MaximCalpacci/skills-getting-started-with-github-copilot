import pytest

@pytest.mark.asyncio
async def test_get_activities(async_client):
    # Arrange: (nothing to arrange for this test)

    # Act
    response = await async_client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

@pytest.mark.asyncio
async def test_signup_and_duplicate(async_client):
    # Arrange
    activity = "Chess Club"
    email = "testuser@mergington.edu"

    # Act: sign up new user
    response_signup = await async_client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response_signup.status_code == 200
    assert f"Signed up {email}" in response_signup.json().get("message", "")

    # Act: try duplicate signup
    response_duplicate = await async_client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response_duplicate.status_code == 400
    assert "already signed up" in response_duplicate.json().get("detail", "")

@pytest.mark.asyncio
async def test_unregister_and_not_registered(async_client):
    # Arrange
    activity = "Chess Club"
    email = "testuser@mergington.edu"

    # Act: unregister user
    response_unreg = await async_client.post(f"/activities/{activity}/unregister?email={email}")

    # Assert
    assert response_unreg.status_code == 200
    assert f"Unregistered {email}" in response_unreg.json().get("message", "")

    # Act: try to unregister again
    response_unreg2 = await async_client.post(f"/activities/{activity}/unregister?email={email}")

    # Assert
    assert response_unreg2.status_code == 400
    assert "not registered" in response_unreg2.json().get("detail", "")
