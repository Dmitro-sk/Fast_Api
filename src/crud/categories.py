from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Category
from src.schemas.category import CategoryCreate, CategoryUpdate


async def create_category(db: AsyncSession, category_in: CategoryCreate) -> Category:
    category = Category(**category_in.model_dump())
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


async def get_category(db: AsyncSession, category_id: int) -> Category | None:
    return await db.get(Category, category_id)


async def get_categories(db: AsyncSession) -> list[Category]:
    result = await db.execute(select(Category).order_by(Category.id))
    return list(result.scalars().all())


async def update_category(db: AsyncSession, category: Category, category_in: CategoryUpdate) -> Category:
    for field, value in category_in.model_dump(exclude_unset=True).items():
        setattr(category, field, value)
    await db.commit()
    await db.refresh(category)
    return category


async def delete_category(db: AsyncSession, category: Category) -> None:
    await db.delete(category)
    await db.commit()
