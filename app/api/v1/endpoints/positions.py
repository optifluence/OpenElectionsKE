from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Position
from app.database import get_db
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class PositionCreate(BaseModel):
    name: str

class PositionRead(PositionCreate):
    id: int
    class Config:
        orm_mode = True

@router.get("/", response_model=List[PositionRead])
async def list_positions(name: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    query = select(Position)
    if name:
        query = query.where(Position.name.ilike(f"%{name}%"))
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/", response_model=PositionRead)
async def create_position(position: PositionCreate, db: AsyncSession = Depends(get_db)):
    db_position = Position(**position.dict())
    db.add(db_position)
    await db.commit()
    await db.refresh(db_position)
    return db_position

@router.get("/{position_id}", response_model=PositionRead)
async def get_position(position_id: int, db: AsyncSession = Depends(get_db)):
    position = await db.get(Position, position_id)
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
    return position

@router.put("/{position_id}", response_model=PositionRead)
async def update_position(position_id: int, position: PositionCreate, db: AsyncSession = Depends(get_db)):
    db_position = await db.get(Position, position_id)
    if not db_position:
        raise HTTPException(status_code=404, detail="Position not found")
    for key, value in position.dict().items():
        setattr(db_position, key, value)
    await db.commit()
    await db.refresh(db_position)
    return db_position

@router.delete("/{position_id}")
async def delete_position(position_id: int, db: AsyncSession = Depends(get_db)):
    position = await db.get(Position, position_id)
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
    await db.delete(position)
    await db.commit()
    return {"ok": True}
