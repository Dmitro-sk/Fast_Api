from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import categories as categories_crud
from src.database import get_async_session
from src.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_in: CategoryCreate,
    db: AsyncSession = Depends(get_async_session),
):
    return await categories_crud.create_category(db, category_in)


@router.get("/", response_model=list[CategoryRead])
async def read_categories(db: AsyncSession = Depends(get_async_session)):
    return await categories_crud.get_categories(db)


@router.get("/{category_id}", response_model=CategoryRead)
async def read_category(category_id: int, db: AsyncSession = Depends(get_async_session)):
    category = await categories_crud.get_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.put("/{category_id}", response_model=CategoryRead)
async def update_category(
    category_id: int,
    category_in: CategoryUpdate,
    db: AsyncSession = Depends(get_async_session),
):
    category = await categories_crud.get_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return await categories_crud.update_category(db, category, category_in)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_async_session)):
    category = await categories_crud.get_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    await categories_crud.delete_category(db, category)
