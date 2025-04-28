from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Election
from app.database import get_db
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter()

class ElectionCreate(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    created_by: int

@router.get("/", response_model=List[ElectionCreate])
async def list_elections(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Election))
    elections = result.scalars().all()
    return elections

@router.post("/", response_model=ElectionCreate)
async def create_election(election: ElectionCreate, db: AsyncSession = Depends(get_db)):
    db_election = Election(**election.dict())
    db.add(db_election)
    await db.commit()
    await db.refresh(db_election)
    return db_election
