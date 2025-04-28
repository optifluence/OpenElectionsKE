from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.models import Result, PollingStation, Ward, Constituency, County, Position, Candidate
from app.database import get_db
from pydantic import BaseModel
from typing import List
from datetime import datetime

router = APIRouter()

class ResultCreate(BaseModel):
    election_id: int
    candidate_id: int
    polling_station_id: int
    position_id: int
    votes: int
    reported_at: datetime = datetime.utcnow()

@router.get("/", response_model=List[ResultCreate])
async def list_results(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Result))
    results = result.scalars().all()
    return results

@router.post("/", response_model=ResultCreate)
async def create_result(result: ResultCreate, db: AsyncSession = Depends(get_db)):
    db_result = Result(**result.dict())
    db.add(db_result)
    await db.commit()
    await db.refresh(db_result)
    return db_result

@router.get("/aggregate")
async def aggregate_results(
    position_id: int,
    election_id: int,
    db: AsyncSession = Depends(get_db)
):
    position = await db.get(Position, position_id)
    if not position:
        raise HTTPException(status_code=404, detail='Position not found')
    level = position.level

    base_query = (
        select(
            Candidate.id.label('candidate_id'),
            Candidate.name.label('candidate_name'),
            func.sum(Result.votes).label('total_votes')
        )
        .join(Result.candidate)
        .join(Result.polling_station)
        .where(Result.position_id == position_id, Result.election_id == election_id)
    )

    if level == 'ward':
        base_query = (
            base_query
            .join(PollingStation.ward)
            .group_by(Ward.id, Candidate.id, Candidate.name)
            .with_only_columns([
                Ward.id.label('location_id'),
                Ward.name.label('location_name'),
                Candidate.id.label('candidate_id'),
                Candidate.name.label('candidate_name'),
                func.sum(Result.votes).label('total_votes')
            ])
        )
    elif level == 'constituency':
        base_query = (
            base_query
            .join(PollingStation.ward)
            .join(Ward.constituency)
            .group_by(Constituency.id, Candidate.id, Candidate.name)
            .with_only_columns([
                Constituency.id.label('location_id'),
                Constituency.name.label('location_name'),
                Candidate.id.label('candidate_id'),
                Candidate.name.label('candidate_name'),
                func.sum(Result.votes).label('total_votes')
            ])
        )
    elif level == 'county':
        base_query = (
            base_query
            .join(PollingStation.ward)
            .join(Ward.constituency)
            .join(Constituency.county)
            .group_by(County.id, Candidate.id, Candidate.name)
            .with_only_columns([
                County.id.label('location_id'),
                County.name.label('location_name'),
                Candidate.id.label('candidate_id'),
                Candidate.name.label('candidate_name'),
                func.sum(Result.votes).label('total_votes')
            ])
        )
    elif level == 'national':
        base_query = (
            base_query
            .group_by(Candidate.id, Candidate.name)
            .with_only_columns([
                Candidate.id.label('candidate_id'),
                Candidate.name.label('candidate_name'),
                func.sum(Result.votes).label('total_votes')
            ])
        )
    else:
        raise HTTPException(status_code=400, detail='Invalid position level')

    result = await db.execute(base_query)
    return [dict(row) for row in result]
