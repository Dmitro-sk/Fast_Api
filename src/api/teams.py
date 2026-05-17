from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import teams as teams_crud
from src.database import get_async_session
from src.schemas.team import TeamCreate, TeamRead, TeamUpdate

router = APIRouter(prefix="/teams", tags=["Teams"])


@router.post("/", response_model=TeamRead, status_code=status.HTTP_201_CREATED)
async def create_team(
    team_in: TeamCreate,
    db: AsyncSession = Depends(get_async_session),
):
    return await teams_crud.create_team(db, team_in)


@router.get("/", response_model=list[TeamRead])
async def read_teams(db: AsyncSession = Depends(get_async_session)):
    return await teams_crud.get_teams(db)


@router.get("/{team_id}", response_model=TeamRead)
async def read_team(team_id: int, db: AsyncSession = Depends(get_async_session)):
    team = await teams_crud.get_team(db, team_id)
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.put("/{team_id}", response_model=TeamRead)
async def update_team(
    team_id: int,
    team_in: TeamUpdate,
    db: AsyncSession = Depends(get_async_session),
):
    team = await teams_crud.get_team(db, team_id)
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return await teams_crud.update_team(db, team, team_in)


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(team_id: int, db: AsyncSession = Depends(get_async_session)):
    team = await teams_crud.get_team(db, team_id)
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    await teams_crud.delete_team(db, team)
