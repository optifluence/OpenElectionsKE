from fastapi import FastAPI
from app.api.v1.endpoints import users, elections, candidates, results, positions, counties, constituencies, wards, polling_stations

application = FastAPI()

application.include_router(users.router, prefix="/api/v1/users", tags=["users"])
application.include_router(elections.router, prefix="/api/v1/elections", tags=["elections"])
application.include_router(candidates.router, prefix="/api/v1/candidates", tags=["candidates"])
application.include_router(results.router, prefix="/api/v1/results", tags=["results"])
application.include_router(positions.router, prefix="/api/v1/positions", tags=["positions"])
application.include_router(counties.router, prefix="/api/v1/counties", tags=["counties"])
application.include_router(constituencies.router, prefix="/api/v1/constituencies", tags=["constituencies"])
application.include_router(wards.router, prefix="/api/v1/wards", tags=["wards"])
application.include_router(polling_stations.router, prefix="/api/v1/polling-stations", tags=["polling_stations"])
