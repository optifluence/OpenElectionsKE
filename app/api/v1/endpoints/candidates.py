from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Candidate
from app.database import get_db
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter()

class CandidateCreate(BaseModel):
    name: str
    election_id: int

@router.get("/", response_model=List[CandidateCreate])
async def list_candidates(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Candidate))
    candidates = result.scalars().all()
    return candidates

@router.post("/", response_model=CandidateCreate)
async def create_candidate(candidate: CandidateCreate, db: AsyncSession = Depends(get_db)):
    db_candidate = Candidate(**candidate.dict())
    db.add(db_candidate)
    await db.commit()
    await db.refresh(db_candidate)
    return db_candidate
