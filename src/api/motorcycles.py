from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import motorcycles as motorcycles_crud
from src.database import get_async_session
from src.schemas.motorcycle import MotorcycleCreate, MotorcycleRead, MotorcycleUpdate

router = APIRouter(prefix="/motorcycles", tags=["Motorcycles"])


@router.post("/", response_model=MotorcycleRead, status_code=status.HTTP_201_CREATED)
async def create_motorcycle(
    motorcycle_in: MotorcycleCreate,
    db: AsyncSession = Depends(get_async_session),
):
    return await motorcycles_crud.create_motorcycle(db, motorcycle_in)


@router.get("/", response_model=list[MotorcycleRead])
async def read_motorcycles(db: AsyncSession = Depends(get_async_session)):
    return await motorcycles_crud.get_motorcycles(db)


@router.get("/{motorcycle_id}", response_model=MotorcycleRead)
async def read_motorcycle(motorcycle_id: int, db: AsyncSession = Depends(get_async_session)):
    motorcycle = await motorcycles_crud.get_motorcycle(db, motorcycle_id)
    if motorcycle is None:
        raise HTTPException(status_code=404, detail="Motorcycle not found")
    return motorcycle


@router.put("/{motorcycle_id}", response_model=MotorcycleRead)
async def update_motorcycle(
    motorcycle_id: int,
    motorcycle_in: MotorcycleUpdate,
    db: AsyncSession = Depends(get_async_session),
):
    motorcycle = await motorcycles_crud.get_motorcycle(db, motorcycle_id)
    if motorcycle is None:
        raise HTTPException(status_code=404, detail="Motorcycle not found")
    return await motorcycles_crud.update_motorcycle(db, motorcycle, motorcycle_in)


@router.delete("/{motorcycle_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_motorcycle(
    motorcycle_id: int,
    db: AsyncSession = Depends(get_async_session),
):
    motorcycle = await motorcycles_crud.get_motorcycle(db, motorcycle_id)
    if motorcycle is None:
        raise HTTPException(status_code=404, detail="Motorcycle not found")
    await motorcycles_crud.delete_motorcycle(db, motorcycle)
