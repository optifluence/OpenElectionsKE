import pytest

@pytest.mark.asyncio
async def test_create_and_get_polling_station(test_app):
    # Create county, constituency, ward first
    county_resp = test_app.post("/api/v1/counties/", json={"name": "PSCounty"})
    county_id = county_resp.json()["id"]
    constituency_resp = test_app.post("/api/v1/constituencies/", json={"name": "PSConstituency", "county_id": county_id})
    constituency_id = constituency_resp.json()["id"]
    ward_resp = test_app.post("/api/v1/wards/", json={"name": "PSWard", "constituency_id": constituency_id})
    ward_id = ward_resp.json()["id"]
    # Create polling station
    response = test_app.post("/api/v1/polling-stations/", json={"name": "TestPS", "ward_id": ward_id})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "TestPS"
    assert data["ward_id"] == ward_id
    ps_id = data["id"]
    # Get
    response = test_app.get(f"/api/v1/polling-stations/{ps_id}")
    assert response.status_code == 200
    assert response.json()["id"] == ps_id

@pytest.mark.asyncio
async def test_list_polling_stations(test_app):
    response = test_app.get("/api/v1/polling-stations/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_update_polling_station(test_app):
    county_resp = test_app.post("/api/v1/counties/", json={"name": "PSUpCounty"})
    county_id = county_resp.json()["id"]
    constituency_resp = test_app.post("/api/v1/constituencies/", json={"name": "PSUpConstituency", "county_id": county_id})
    constituency_id = constituency_resp.json()["id"]
    ward_resp = test_app.post("/api/v1/wards/", json={"name": "PSUpWard", "constituency_id": constituency_id})
    ward_id = ward_resp.json()["id"]
    response = test_app.post("/api/v1/polling-stations/", json={"name": "ToUpdatePS", "ward_id": ward_id})
    ps_id = response.json()["id"]
    response = test_app.put(f"/api/v1/polling-stations/{ps_id}", json={"name": "UpdatedPS", "ward_id": ward_id})
    assert response.status_code == 200
    assert response.json()["name"] == "UpdatedPS"

@pytest.mark.asyncio
async def test_delete_polling_station(test_app):
    county_resp = test_app.post("/api/v1/counties/", json={"name": "PSDelCounty"})
    county_id = county_resp.json()["id"]
    constituency_resp = test_app.post("/api/v1/constituencies/", json={"name": "PSDelConstituency", "county_id": county_id})
    constituency_id = constituency_resp.json()["id"]
    ward_resp = test_app.post("/api/v1/wards/", json={"name": "PSDelWard", "constituency_id": constituency_id})
    ward_id = ward_resp.json()["id"]
    response = test_app.post("/api/v1/polling-stations/", json={"name": "ToDeletePS", "ward_id": ward_id})
    ps_id = response.json()["id"]
    response = test_app.delete(f"/api/v1/polling-stations/{ps_id}")
    assert response.status_code == 200
    response = test_app.get(f"/api/v1/polling-stations/{ps_id}")
    assert response.status_code == 404
