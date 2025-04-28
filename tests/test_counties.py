import pytest

@pytest.mark.asyncio
async def test_create_and_get_county(test_app):
    # Create a county
    response = test_app.post("/api/v1/counties/", json={"name": "Nairobi"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Nairobi"
    county_id = data["id"]

    # Get county by ID
    response = test_app.get(f"/api/v1/counties/{county_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == county_id
    assert data["name"] == "Nairobi"

@pytest.mark.asyncio
async def test_list_counties(test_app):
    # List counties (should contain at least one from previous test)
    response = test_app.get("/api/v1/counties/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(county["name"] == "Nairobi" for county in data)

@pytest.mark.asyncio
async def test_update_county(test_app):
    # Create a county
    response = test_app.post("/api/v1/counties/", json={"name": "Kisumu"})
    county_id = response.json()["id"]
    # Update county
    response = test_app.put(f"/api/v1/counties/{county_id}", json={"name": "Kisumu Updated"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Kisumu Updated"

@pytest.mark.asyncio
async def test_delete_county(test_app):
    # Create a county
    response = test_app.post("/api/v1/counties/", json={"name": "DeleteMe"})
    county_id = response.json()["id"]
    # Delete
    response = test_app.delete(f"/api/v1/counties/{county_id}")
    assert response.status_code == 200
    # Ensure deleted
    response = test_app.get(f"/api/v1/counties/{county_id}")
    assert response.status_code == 404
