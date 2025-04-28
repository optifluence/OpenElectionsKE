from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import PollingStation
from app.database import get_db
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class PollingStationCreate(BaseModel):
    name: str
    code: Optional[str] = None
    ward_id: int

class PollingStationRead(PollingStationCreate):
    id: int
    class Config:
        orm_mode = True

@router.get("/", response_model=List[PollingStationRead])
async def list_polling_stations(ward_id: Optional[int] = None, db: AsyncSession = Depends(get_db)):
    query = select(PollingStation)
    if ward_id:
        query = query.where(PollingStation.ward_id == ward_id)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/", response_model=PollingStationRead)
async def create_polling_station(station: PollingStationCreate, db: AsyncSession = Depends(get_db)):
    db_station = PollingStation(**station.dict())
    db.add(db_station)
    await db.commit()
    await db.refresh(db_station)
    return db_station

@router.get("/{station_id}", response_model=PollingStationRead)
async def get_polling_station(station_id: int, db: AsyncSession = Depends(get_db)):
    station = await db.get(PollingStation, station_id)
    if not station:
        raise HTTPException(status_code=404, detail="Polling station not found")
    return station

@router.put("/{station_id}", response_model=PollingStationRead)
async def update_polling_station(station_id: int, station: PollingStationCreate, db: AsyncSession = Depends(get_db)):
    db_station = await db.get(PollingStation, station_id)
    if not db_station:
        raise HTTPException(status_code=404, detail="Polling station not found")
    for key, value in station.dict().items():
        setattr(db_station, key, value)
    await db.commit()
    await db.refresh(db_station)
    return db_station

@router.delete("/{station_id}")
async def delete_polling_station(station_id: int, db: AsyncSession = Depends(get_db)):
    station = await db.get(PollingStation, station_id)
    if not station:
        raise HTTPException(status_code=404, detail="Polling station not found")
    await db.delete(station)
    await db.commit()
    return {"ok": True}
