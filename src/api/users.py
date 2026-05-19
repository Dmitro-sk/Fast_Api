from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import motorcycles as motorcycles_crud
from src.crud import users as users_crud
from src.database import get_async_session
from src.models import User
from src.schemas.motorcycle import MotorcycleRead
from src.schemas.user import UserCreate, UserRead, UserUpdate
from src.security import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_async_session),
):
    return await users_crud.create_user(db, user_in)


@router.get("/", response_model=list[UserRead])
async def read_users(db: AsyncSession = Depends(get_async_session)):
    return await users_crud.get_users(db)


@router.get("/me", response_model=UserRead)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/me/motorcycles", response_model=list[MotorcycleRead])
async def read_current_user_motorcycles(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    return await motorcycles_crud.get_motorcycles_by_owner(db, current_user.id)


@router.get("/{user_id}", response_model=UserRead)
async def read_user(user_id: int, db: AsyncSession = Depends(get_async_session)):
    user = await users_crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_async_session),
):
    user = await users_crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return await users_crud.update_user(db, user, user_in)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_async_session)):
    user = await users_crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await users_crud.delete_user(db, user)
