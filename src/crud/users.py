from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User
from src.schemas.user import UserCreate, UserUpdate
from src.security import hash_password


async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    user_data = user_in.model_dump()
    user_data["password"] = hash_password(user_data["password"])
    user = User(**user_data)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_user(db: AsyncSession, user_id: int) -> User | None:
    return await db.get(User, user_id)


async def get_users(db: AsyncSession) -> list[User]:
    result = await db.execute(select(User).order_by(User.id))
    return list(result.scalars().all())


async def get_user_by_username_or_email(db: AsyncSession, username_or_email: str) -> User | None:
    result = await db.execute(
        select(User).where(
            (User.username == username_or_email) | (User.email == username_or_email),
        ),
    )
    return result.scalar_one_or_none()


async def update_user(db: AsyncSession, user: User, user_in: UserUpdate) -> User:
    for field, value in user_in.model_dump(exclude_unset=True).items():
        if field == "password":
            value = hash_password(value)
        setattr(user, field, value)
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user: User) -> None:
    await db.delete(user)
    await db.commit()
