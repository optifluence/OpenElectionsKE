from fastapi import FastAPI
from app.api.v1.endpoints import users, elections

app = FastAPI()

app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(elections.router, prefix="/api/v1/elections", tags=["elections"])
