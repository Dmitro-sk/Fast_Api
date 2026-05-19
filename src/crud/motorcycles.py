from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Motorcycle
from src.schemas.motorcycle import MotorcycleCreate, MotorcycleUpdate


async def create_motorcycle(db: AsyncSession, motorcycle_in: MotorcycleCreate) -> Motorcycle:
    motorcycle = Motorcycle(**motorcycle_in.model_dump())
    db.add(motorcycle)
    await db.commit()
    await db.refresh(motorcycle)
    return motorcycle


async def get_motorcycle(db: AsyncSession, motorcycle_id: int) -> Motorcycle | None:
    return await db.get(Motorcycle, motorcycle_id)


async def get_motorcycles(db: AsyncSession) -> list[Motorcycle]:
    result = await db.execute(select(Motorcycle).order_by(Motorcycle.id))
    return list(result.scalars().all())


async def get_motorcycles_by_owner(db: AsyncSession, owner_id: int) -> list[Motorcycle]:
    result = await db.execute(
        select(Motorcycle).where(Motorcycle.owner_id == owner_id).order_by(Motorcycle.id),
    )
    return list(result.scalars().all())


async def update_motorcycle(
    db: AsyncSession,
    motorcycle: Motorcycle,
    motorcycle_in: MotorcycleUpdate,
) -> Motorcycle:
    for field, value in motorcycle_in.model_dump(exclude_unset=True).items():
        setattr(motorcycle, field, value)
    await db.commit()
    await db.refresh(motorcycle)
    return motorcycle


async def delete_motorcycle(db: AsyncSession, motorcycle: Motorcycle) -> None:
    await db.delete(motorcycle)
    await db.commit()
