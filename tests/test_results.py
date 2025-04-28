import pytest
from datetime import datetime

@pytest.mark.asyncio
async def test_create_and_get_result(test_app):
    # Setup: create all required foreign keys
    county = test_app.post("/api/v1/counties/", json={"name": "ResCounty"}).json()
    constituency = test_app.post("/api/v1/constituencies/", json={"name": "ResConstituency", "county_id": county["id"]}).json()
    ward = test_app.post("/api/v1/wards/", json={"name": "ResWard", "constituency_id": constituency["id"]}).json()
    station = test_app.post("/api/v1/polling-stations/", json={"name": "ResStation", "ward_id": ward["id"]}).json()
    position = test_app.post("/api/v1/positions/", json={"name": "President", "level": "national"}).json()
    candidate = test_app.post("/api/v1/candidates/", json={"name": "John Doe", "position_id": position["id"]}).json()
    election = test_app.post("/api/v1/elections/", json={"name": "2027 General"}).json()
    # Create result
    payload = {
        "election_id": election["id"],
        "candidate_id": candidate["id"],
        "polling_station_id": station["id"],
        "position_id": position["id"],
        "votes": 123,
        "reported_at": datetime.utcnow().isoformat()
    }
    response = test_app.post("/api/v1/results/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["votes"] == 123
    assert data["candidate_id"] == candidate["id"]

@pytest.mark.asyncio
async def test_list_results(test_app):
    response = test_app.get("/api/v1/results/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
