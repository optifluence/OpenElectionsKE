import pytest

@pytest.mark.asyncio
async def test_create_and_get_constituency(test_app):
    # First, create a county for the constituency
    county_resp = test_app.post("/api/v1/counties/", json={"name": "TestCounty"})
    county_id = county_resp.json()["id"]
    # Create constituency
    response = test_app.post("/api/v1/constituencies/", json={"name": "TestConstituency", "county_id": county_id})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "TestConstituency"
    assert data["county_id"] == county_id
    constituency_id = data["id"]
    # Get
    response = test_app.get(f"/api/v1/constituencies/{constituency_id}")
    assert response.status_code == 200
    assert response.json()["id"] == constituency_id

@pytest.mark.asyncio
async def test_list_constituencies(test_app):
    response = test_app.get("/api/v1/constituencies/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_update_constituency(test_app):
    county_resp = test_app.post("/api/v1/counties/", json={"name": "UpdateCounty"})
    county_id = county_resp.json()["id"]
    response = test_app.post("/api/v1/constituencies/", json={"name": "ToUpdate", "county_id": county_id})
    constituency_id = response.json()["id"]
    response = test_app.put(f"/api/v1/constituencies/{constituency_id}", json={"name": "Updated", "county_id": county_id})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated"

@pytest.mark.asyncio
async def test_delete_constituency(test_app):
    county_resp = test_app.post("/api/v1/counties/", json={"name": "DeleteCounty"})
    county_id = county_resp.json()["id"]
    response = test_app.post("/api/v1/constituencies/", json={"name": "ToDelete", "county_id": county_id})
    constituency_id = response.json()["id"]
    response = test_app.delete(f"/api/v1/constituencies/{constituency_id}")
    assert response.status_code == 200
    response = test_app.get(f"/api/v1/constituencies/{constituency_id}")
    assert response.status_code == 404
