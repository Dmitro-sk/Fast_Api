from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src.models import Motorcycle, Category, User

router = APIRouter(prefix="/motorcycles", tags=["Motorcycles"])

@router.post("/{user_id}/motorcycles")
async def add_motorcycle(
    user_id: int, model_name: str, year: int, category_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")

    new_moto = Motorcycle(model_name=model_name, year=year, owner_id=user_id, category_id=category_id)
    db.add(new_moto)
    await db.commit()
    await db.refresh(new_moto)
    return {"status": "success", "id": new_moto.id}

@router.post("/category")
async def create_category(name: str, db: AsyncSession = Depends(get_async_session)):
    new_cat = Category(name=name)
    db.add(new_cat)
    await db.commit()
    await db.refresh(new_cat)
    return new_cat