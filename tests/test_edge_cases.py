import pytest
from datetime import datetime

@pytest.mark.asyncio
async def test_create_county_duplicate_name(test_app):
    resp1 = test_app.post("/api/v1/counties/", json={"name": "UniqueCounty"})
    assert resp1.status_code == 200
    resp2 = test_app.post("/api/v1/counties/", json={"name": "UniqueCounty"})
    assert resp2.status_code in (400, 409)

@pytest.mark.asyncio
async def test_create_county_empty_name(test_app):
    resp = test_app.post("/api/v1/counties/", json={"name": ""})
    assert resp.status_code in (400, 422)

@pytest.mark.asyncio
async def test_get_nonexistent_county(test_app):
    resp = test_app.get("/api/v1/counties/99999")
    assert resp.status_code == 404

@pytest.mark.asyncio
async def test_delete_nonexistent_county(test_app):
    resp = test_app.delete("/api/v1/counties/99999")
    assert resp.status_code == 404

@pytest.mark.asyncio
async def test_create_constituency_invalid_fk(test_app):
    resp = test_app.post("/api/v1/constituencies/", json={"name": "Bad", "county_id": 99999})
    assert resp.status_code in (400, 422, 404)

@pytest.mark.asyncio
async def test_update_constituency_invalid_data(test_app):
    # Create valid county and constituency
    county = test_app.post("/api/v1/counties/", json={"name": "ValidCounty"}).json()
    resp = test_app.post("/api/v1/constituencies/", json={"name": "ValidCon", "county_id": county["id"]})
    con_id = resp.json()["id"]
    # Try to update with missing name
    resp = test_app.put(f"/api/v1/constituencies/{con_id}", json={"name": "", "county_id": county["id"]})
    assert resp.status_code in (400, 422)

@pytest.mark.asyncio
async def test_create_ward_invalid_fk(test_app):
    resp = test_app.post("/api/v1/wards/", json={"name": "BadWard", "constituency_id": 99999})
    assert resp.status_code in (400, 422, 404)

@pytest.mark.asyncio
async def test_create_polling_station_invalid_fk(test_app):
    resp = test_app.post("/api/v1/polling-stations/", json={"name": "BadPS", "ward_id": 99999})
    assert resp.status_code in (400, 422, 404)

@pytest.mark.asyncio
async def test_create_position_duplicate_name(test_app):
    resp1 = test_app.post("/api/v1/positions/", json={"name": "President", "level": "national"})
    assert resp1.status_code == 200
    resp2 = test_app.post("/api/v1/positions/", json={"name": "President", "level": "national"})
    assert resp2.status_code in (400, 409)

@pytest.mark.asyncio
async def test_create_result_negative_votes(test_app):
    # Setup valid FKs
    county = test_app.post("/api/v1/counties/", json={"name": "NegResCounty"}).json()
    constituency = test_app.post("/api/v1/constituencies/", json={"name": "NegResCon", "county_id": county["id"]}).json()
    ward = test_app.post("/api/v1/wards/", json={"name": "NegResWard", "constituency_id": constituency["id"]}).json()
    station = test_app.post("/api/v1/polling-stations/", json={"name": "NegResStation", "ward_id": ward["id"]}).json()
    position = test_app.post("/api/v1/positions/", json={"name": "NegResPos", "level": "ward"}).json()
    candidate = test_app.post("/api/v1/candidates/", json={"name": "NegResCand", "position_id": position["id"]}).json()
    election = test_app.post("/api/v1/elections/", json={"name": "NegResElection"}).json()
    payload = {
        "election_id": election["id"],
        "candidate_id": candidate["id"],
        "polling_station_id": station["id"],
        "position_id": position["id"],
        "votes": -5,
        "reported_at": datetime.utcnow().isoformat()
    }
    resp = test_app.post("/api/v1/results/", json=payload)
    assert resp.status_code in (400, 422)

@pytest.mark.asyncio
async def test_aggregate_no_results(test_app):
    # Setup valid FKs
    county = test_app.post("/api/v1/counties/", json={"name": "EmptyAggCounty"}).json()
    position = test_app.post("/api/v1/positions/", json={"name": "EmptyAggPos", "level": "county"}).json()
    election = test_app.post("/api/v1/elections/", json={"name": "EmptyAggElection"}).json()
    resp = test_app.get(f"/api/v1/results/aggregate?position_id={position['id']}&election_id={election['id']}")
    assert resp.status_code == 200
    assert resp.json() == []

@pytest.mark.asyncio
async def test_aggregate_invalid_position(test_app):
    election = test_app.post("/api/v1/elections/", json={"name": "BadAggElection"}).json()
    resp = test_app.get(f"/api/v1/results/aggregate?position_id=99999&election_id={election['id']}")
    assert resp.status_code == 404
