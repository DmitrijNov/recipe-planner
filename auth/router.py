from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from auth.schemas import (
    LoginUserSchema,
    RefreshTokenRequest,
    RegisterReqSchema,
    TokenResponse,
)
from auth.services.auth import AuthService, TokenService
from core.database import db

auth_router = APIRouter(prefix="/auth")
auth_service = AuthService(token_service=TokenService())


@auth_router.post("/login", response_model=TokenResponse)
async def login(
    login_data: LoginUserSchema,
    session: AsyncSession = Depends(db.session),
):
    tokens = await auth_service.authenticate(login_data=login_data, session=session)
    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid username or password",
        )
    return tokens


@auth_router.post("/refresh", response_model=TokenResponse)
async def refresh(
    payload: RefreshTokenRequest,
    session: AsyncSession = Depends(db.session),
):
    tokens = await auth_service.refresh(
        refresh_token=payload.refresh_token,
        session=session,
    )
    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid refresh token",
        )
    return tokens


@auth_router.post("/register", response_model=TokenResponse)
async def register(
    user: RegisterReqSchema, session: AsyncSession = Depends(db.session)
):
    tokens = await auth_service.register(user_data=user, session=session)
    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="user already exists",
        )
    return tokens
