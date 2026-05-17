from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import profiles as profiles_crud
from src.database import get_async_session
from src.schemas.profile import ProfileCreate, ProfileRead, ProfileUpdate

router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.post("/", response_model=ProfileRead, status_code=status.HTTP_201_CREATED)
async def create_profile(
    profile_in: ProfileCreate,
    db: AsyncSession = Depends(get_async_session),
):
    return await profiles_crud.create_profile(db, profile_in)


@router.get("/", response_model=list[ProfileRead])
async def read_profiles(db: AsyncSession = Depends(get_async_session)):
    return await profiles_crud.get_profiles(db)


@router.get("/{profile_id}", response_model=ProfileRead)
async def read_profile(profile_id: int, db: AsyncSession = Depends(get_async_session)):
    profile = await profiles_crud.get_profile(db, profile_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.put("/{profile_id}", response_model=ProfileRead)
async def update_profile(
    profile_id: int,
    profile_in: ProfileUpdate,
    db: AsyncSession = Depends(get_async_session),
):
    profile = await profiles_crud.get_profile(db, profile_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return await profiles_crud.update_profile(db, profile, profile_in)


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(profile_id: int, db: AsyncSession = Depends(get_async_session)):
    profile = await profiles_crud.get_profile(db, profile_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    await profiles_crud.delete_profile(db, profile)
