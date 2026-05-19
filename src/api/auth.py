from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import users as users_crud
from src.database import get_async_session
from src.models import User
from src.schemas.auth import AuthResponse, LoginRequest
from src.schemas.user import UserCreate, UserRead
from src.security import create_access_token, get_current_user, verify_password
from src.config import settings

router = APIRouter(prefix="/auth", tags=["Auth"])


def set_auth_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key=settings.AUTH_COOKIE_NAME,
        value=token,
        httponly=True,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserCreate,
    response: Response,
    db: AsyncSession = Depends(get_async_session),
):
    try:
        user = await users_crud.create_user(db, user_in)
    except IntegrityError as exc:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this username or email already exists",
        ) from exc

    set_auth_cookie(response, create_access_token(str(user.id)))
    return AuthResponse(message="Registered successfully", user=UserRead.model_validate(user))


@router.post("/login", response_model=AuthResponse)
async def login(
    login_in: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_async_session),
):
    user = await users_crud.get_user_by_username_or_email(db, login_in.username)
    if user is None or not verify_password(login_in.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    set_auth_cookie(response, create_access_token(str(user.id)))
    return AuthResponse(message="Logged in successfully", user=UserRead.model_validate(user))


@router.post("/logout")
async def logout(response: Response) -> dict[str, str]:
    response.delete_cookie(settings.AUTH_COOKIE_NAME)
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserRead)
async def read_auth_user(current_user: User = Depends(get_current_user)):
    return current_user
