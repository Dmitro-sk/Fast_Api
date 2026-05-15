from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database import get_async_session
from src.models import User

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/")
async def create_user(username: str, email: str, password: str, db: AsyncSession = Depends(get_async_session)):
    new_user = User(username=username, email=email, password=password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.get("/")
async def get_users(db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(User))
    return result.scalars().all()