from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Ward
from app.database import get_db
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class WardCreate(BaseModel):
    name: str
    constituency_id: int

class WardRead(WardCreate):
    id: int
    class Config:
        orm_mode = True

@router.get("/", response_model=List[WardRead])
async def list_wards(constituency_id: Optional[int] = None, db: AsyncSession = Depends(get_db)):
    query = select(Ward)
    if constituency_id:
        query = query.where(Ward.constituency_id == constituency_id)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/", response_model=WardRead)
async def create_ward(ward: WardCreate, db: AsyncSession = Depends(get_db)):
    db_ward = Ward(**ward.dict())
    db.add(db_ward)
    await db.commit()
    await db.refresh(db_ward)
    return db_ward

@router.get("/{ward_id}", response_model=WardRead)
async def get_ward(ward_id: int, db: AsyncSession = Depends(get_db)):
    ward = await db.get(Ward, ward_id)
    if not ward:
        raise HTTPException(status_code=404, detail="Ward not found")
    return ward

@router.put("/{ward_id}", response_model=WardRead)
async def update_ward(ward_id: int, ward: WardCreate, db: AsyncSession = Depends(get_db)):
    db_ward = await db.get(Ward, ward_id)
    if not db_ward:
        raise HTTPException(status_code=404, detail="Ward not found")
    for key, value in ward.dict().items():
        setattr(db_ward, key, value)
    await db.commit()
    await db.refresh(db_ward)
    return db_ward

@router.delete("/{ward_id}")
async def delete_ward(ward_id: int, db: AsyncSession = Depends(get_db)):
    ward = await db.get(Ward, ward_id)
    if not ward:
        raise HTTPException(status_code=404, detail="Ward not found")
    await db.delete(ward)
    await db.commit()
    return {"ok": True}
