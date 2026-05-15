from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str # Для створення

class UserResponse(UserBase):
    id: int
    class Config:
        from_attributes = True # Це дозволяє Pydantic читати дані з моделей SQLAlchemy