import pytest

@pytest.mark.asyncio
async def test_create_and_get_position(test_app):
    response = test_app.post("/api/v1/positions/", json={"name": "Governor", "level": "county"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Governor"
    assert data["level"] == "county"
    pos_id = data["id"]
    # Get
    response = test_app.get(f"/api/v1/positions/{pos_id}")
    assert response.status_code == 200
    assert response.json()["id"] == pos_id

@pytest.mark.asyncio
async def test_list_positions(test_app):
    response = test_app.get("/api/v1/positions/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_update_position(test_app):
    response = test_app.post("/api/v1/positions/", json={"name": "MP", "level": "constituency"})
    pos_id = response.json()["id"]
    response = test_app.put(f"/api/v1/positions/{pos_id}", json={"name": "Member of Parliament", "level": "constituency"})
    assert response.status_code == 200
    assert response.json()["name"] == "Member of Parliament"

@pytest.mark.asyncio
async def test_delete_position(test_app):
    response = test_app.post("/api/v1/positions/", json={"name": "DeleteMe", "level": "ward"})
    pos_id = response.json()["id"]
    response = test_app.delete(f"/api/v1/positions/{pos_id}")
    assert response.status_code == 200
    response = test_app.get(f"/api/v1/positions/{pos_id}")
    assert response.status_code == 404
