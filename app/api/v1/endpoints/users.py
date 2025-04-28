from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import User
from app.database import get_db

router = APIRouter()

@router.get("/")
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

@router.post("/")
async def create_user(username: str, email: str, password: str, db: AsyncSession = Depends(get_db)):
    user = User(username=username, email=email, hashed_password=password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
