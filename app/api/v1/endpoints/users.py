# Placeholder for user endpoints
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_users():
    return {"msg": "List users (placeholder)"}
