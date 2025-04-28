import pytest
from datetime import datetime

@pytest.mark.asyncio
async def test_aggregation_endpoint(test_app):
    # Setup: create all hierarchy and a candidate/position for aggregation
    county = test_app.post("/api/v1/counties/", json={"name": "AggCounty"}).json()
    constituency = test_app.post("/api/v1/constituencies/", json={"name": "AggConstituency", "county_id": county["id"]}).json()
    ward = test_app.post("/api/v1/wards/", json={"name": "AggWard", "constituency_id": constituency["id"]}).json()
    station = test_app.post("/api/v1/polling-stations/", json={"name": "AggStation", "ward_id": ward["id"]}).json()
    position = test_app.post("/api/v1/positions/", json={"name": "MCA", "level": "ward"}).json()
    candidate = test_app.post("/api/v1/candidates/", json={"name": "Jane Doe", "position_id": position["id"]}).json()
    election = test_app.post("/api/v1/elections/", json={"name": "2027 General"}).json()
    # Create multiple results for the same candidate in the same ward
    for votes in [100, 150]:
        payload = {
            "election_id": election["id"],
            "candidate_id": candidate["id"],
            "polling_station_id": station["id"],
            "position_id": position["id"],
            "votes": votes,
            "reported_at": datetime.utcnow().isoformat()
        }
        resp = test_app.post("/api/v1/results/", json=payload)
        assert resp.status_code == 200
    # Aggregate by ward (since MCA)
    response = test_app.get(f"/api/v1/results/aggregate?position_id={position['id']}&election_id={election['id']}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Should sum votes (100+150)
    found = False
    for row in data:
        if row["candidate_id"] == candidate["id"] and row["location_id"] == ward["id"]:
            assert row["total_votes"] == 250
            found = True
    assert found
