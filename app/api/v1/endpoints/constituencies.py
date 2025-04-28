from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Constituency
from app.database import get_db
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class ConstituencyCreate(BaseModel):
    name: str
    county_id: int

class ConstituencyRead(ConstituencyCreate):
    id: int
    class Config:
        orm_mode = True

@router.get("/", response_model=List[ConstituencyRead])
async def list_constituencies(county_id: Optional[int] = None, db: AsyncSession = Depends(get_db)):
    query = select(Constituency)
    if county_id:
        query = query.where(Constituency.county_id == county_id)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/", response_model=ConstituencyRead)
async def create_constituency(constituency: ConstituencyCreate, db: AsyncSession = Depends(get_db)):
    db_constituency = Constituency(**constituency.dict())
    db.add(db_constituency)
    await db.commit()
    await db.refresh(db_constituency)
    return db_constituency

@router.get("/{constituency_id}", response_model=ConstituencyRead)
async def get_constituency(constituency_id: int, db: AsyncSession = Depends(get_db)):
    constituency = await db.get(Constituency, constituency_id)
    if not constituency:
        raise HTTPException(status_code=404, detail="Constituency not found")
    return constituency

@router.put("/{constituency_id}", response_model=ConstituencyRead)
async def update_constituency(constituency_id: int, constituency: ConstituencyCreate, db: AsyncSession = Depends(get_db)):
    db_constituency = await db.get(Constituency, constituency_id)
    if not db_constituency:
        raise HTTPException(status_code=404, detail="Constituency not found")
    for key, value in constituency.dict().items():
        setattr(db_constituency, key, value)
    await db.commit()
    await db.refresh(db_constituency)
    return db_constituency

@router.delete("/{constituency_id}")
async def delete_constituency(constituency_id: int, db: AsyncSession = Depends(get_db)):
    constituency = await db.get(Constituency, constituency_id)
    if not constituency:
        raise HTTPException(status_code=404, detail="Constituency not found")
    await db.delete(constituency)
    await db.commit()
    return {"ok": True}
