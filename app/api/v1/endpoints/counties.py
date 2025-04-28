from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import County
from app.database import get_db
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class CountyCreate(BaseModel):
    name: str

class CountyRead(CountyCreate):
    id: int
    class Config:
        orm_mode = True

@router.get("/", response_model=List[CountyRead])
async def list_counties(name: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    query = select(County)
    if name:
        query = query.where(County.name.ilike(f"%{name}%"))
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/", response_model=CountyRead)
async def create_county(county: CountyCreate, db: AsyncSession = Depends(get_db)):
    db_county = County(**county.dict())
    db.add(db_county)
    await db.commit()
    await db.refresh(db_county)
    return db_county

@router.get("/{county_id}", response_model=CountyRead)
async def get_county(county_id: int, db: AsyncSession = Depends(get_db)):
    county = await db.get(County, county_id)
    if not county:
        raise HTTPException(status_code=404, detail="County not found")
    return county

@router.put("/{county_id}", response_model=CountyRead)
async def update_county(county_id: int, county: CountyCreate, db: AsyncSession = Depends(get_db)):
    db_county = await db.get(County, county_id)
    if not db_county:
        raise HTTPException(status_code=404, detail="County not found")
    for key, value in county.dict().items():
        setattr(db_county, key, value)
    await db.commit()
    await db.refresh(db_county)
    return db_county

@router.delete("/{county_id}")
async def delete_county(county_id: int, db: AsyncSession = Depends(get_db)):
    county = await db.get(County, county_id)
    if not county:
        raise HTTPException(status_code=404, detail="County not found")
    await db.delete(county)
    await db.commit()
    return {"ok": True}
