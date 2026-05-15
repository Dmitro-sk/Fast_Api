import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.api.motorcycles import router as moto_router
from src.api.users import router as user_router
from src.database import engine
from src.models import Base

# 1. Налаштовуємо створення таблиць через Lifespan
@asynccontextmanager
async def lifespan(_: FastAPI):
    # Цей блок виконується при запуску додатка
    async with engine.begin() as conn:
        # Створюємо всі таблиці в базі даних автоматично
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Тут можна додати логіку при вимкненні (якщо треба)

# 2. Створюємо додаток з підтримкою lifespan
app = FastAPI(
    title="RaceHub API",
    lifespan=lifespan
)

# 3. Підключаємо роутери
app.include_router(user_router)
app.include_router(moto_router)


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)