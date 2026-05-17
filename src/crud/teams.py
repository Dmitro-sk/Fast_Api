from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Team
from src.schemas.team import TeamCreate, TeamUpdate


async def create_team(db: AsyncSession, team_in: TeamCreate) -> Team:
    team = Team(**team_in.model_dump())
    db.add(team)
    await db.commit()
    await db.refresh(team)
    return team


async def get_team(db: AsyncSession, team_id: int) -> Team | None:
    return await db.get(Team, team_id)


async def get_teams(db: AsyncSession) -> list[Team]:
    result = await db.execute(select(Team).order_by(Team.id))
    return list(result.scalars().all())


async def update_team(db: AsyncSession, team: Team, team_in: TeamUpdate) -> Team:
    for field, value in team_in.model_dump(exclude_unset=True).items():
        setattr(team, field, value)
    await db.commit()
    await db.refresh(team)
    return team


async def delete_team(db: AsyncSession, team: Team) -> None:
    await db.delete(team)
    await db.commit()
