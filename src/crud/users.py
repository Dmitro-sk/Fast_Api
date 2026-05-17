from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User
from src.schemas.user import UserCreate, UserUpdate


async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    user = User(**user_in.model_dump())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_user(db: AsyncSession, user_id: int) -> User | None:
    return await db.get(User, user_id)


async def get_users(db: AsyncSession) -> list[User]:
    result = await db.execute(select(User).order_by(User.id))
    return list(result.scalars().all())


async def update_user(db: AsyncSession, user: User, user_in: UserUpdate) -> User:
    for field, value in user_in.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user: User) -> None:
    await db.delete(user)
    await db.commit()
