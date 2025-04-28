import pytest

@pytest.mark.asyncio
async def test_create_and_get_ward(test_app):
    # Create county and constituency first
    county_resp = test_app.post("/api/v1/counties/", json={"name": "WardCounty"})
    county_id = county_resp.json()["id"]
    constituency_resp = test_app.post("/api/v1/constituencies/", json={"name": "WardConstituency", "county_id": county_id})
    constituency_id = constituency_resp.json()["id"]
    # Create ward
    response = test_app.post("/api/v1/wards/", json={"name": "TestWard", "constituency_id": constituency_id})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "TestWard"
    assert data["constituency_id"] == constituency_id
    ward_id = data["id"]
    # Get
    response = test_app.get(f"/api/v1/wards/{ward_id}")
    assert response.status_code == 200
    assert response.json()["id"] == ward_id

@pytest.mark.asyncio
async def test_list_wards(test_app):
    response = test_app.get("/api/v1/wards/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_update_ward(test_app):
    county_resp = test_app.post("/api/v1/counties/", json={"name": "WardUpCounty"})
    county_id = county_resp.json()["id"]
    constituency_resp = test_app.post("/api/v1/constituencies/", json={"name": "WardUpConstituency", "county_id": county_id})
    constituency_id = constituency_resp.json()["id"]
    response = test_app.post("/api/v1/wards/", json={"name": "ToUpdateWard", "constituency_id": constituency_id})
    ward_id = response.json()["id"]
    response = test_app.put(f"/api/v1/wards/{ward_id}", json={"name": "UpdatedWard", "constituency_id": constituency_id})
    assert response.status_code == 200
    assert response.json()["name"] == "UpdatedWard"

@pytest.mark.asyncio
async def test_delete_ward(test_app):
    county_resp = test_app.post("/api/v1/counties/", json={"name": "WardDelCounty"})
    county_id = county_resp.json()["id"]
    constituency_resp = test_app.post("/api/v1/constituencies/", json={"name": "WardDelConstituency", "county_id": county_id})
    constituency_id = constituency_resp.json()["id"]
    response = test_app.post("/api/v1/wards/", json={"name": "ToDeleteWard", "constituency_id": constituency_id})
    ward_id = response.json()["id"]
    response = test_app.delete(f"/api/v1/wards/{ward_id}")
    assert response.status_code == 200
    response = test_app.get(f"/api/v1/wards/{ward_id}")
    assert response.status_code == 404
