from pydantic import BaseModel, Field

from src.schemas.user import UserRead


class LoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=6, max_length=100)


class AuthResponse(BaseModel):
    message: str
    user: UserRead
