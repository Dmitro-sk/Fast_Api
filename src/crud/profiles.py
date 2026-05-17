from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Profile
from src.schemas.profile import ProfileCreate, ProfileUpdate


async def create_profile(db: AsyncSession, profile_in: ProfileCreate) -> Profile:
    profile = Profile(**profile_in.model_dump())
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    return profile


async def get_profile(db: AsyncSession, profile_id: int) -> Profile | None:
    return await db.get(Profile, profile_id)


async def get_profiles(db: AsyncSession) -> list[Profile]:
    result = await db.execute(select(Profile).order_by(Profile.id))
    return list(result.scalars().all())


async def update_profile(db: AsyncSession, profile: Profile, profile_in: ProfileUpdate) -> Profile:
    for field, value in profile_in.model_dump(exclude_unset=True).items():
        setattr(profile, field, value)
    await db.commit()
    await db.refresh(profile)
    return profile


async def delete_profile(db: AsyncSession, profile: Profile) -> None:
    await db.delete(profile)
    await db.commit()
