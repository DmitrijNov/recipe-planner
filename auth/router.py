import datetime

from fastapi import Depends, HTTPException, Request, status
from fastapi.routing import Router
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from auth.schemas import LoginPayloadSchema, RegisterUserSchema, Token
from auth.security.passwords import hash_password
from core.database import db
from users.models import User

auth_router = Router(prefix="/auth")


@auth_router.post("/login", response_model=Token)
async def login(
    request: Request,
    login_data: LoginPayloadSchema,
    session: AsyncSession = Depends(db.session),
):
    user = await session.get(User, username=login_data.username)
    if not user:
        # todo: make a service for it
        ...
    return False


@auth_router.post("/register")
async def register(
    user: RegisterUserSchema, session: AsyncSession = Depends(db.session)
):
    CONSTRAINT_MESSAGES = {
        "uq_users_email": "Email already registered",
        "uq_users_username": "Username already taken",
    }

    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password),
        created_at=datetime.datetime.now(tz=datetime.UTC),
    )
    session.add(db_user)

    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        name = getattr(exc.orig, "constraint_name", None) or getattr(
            getattr(exc.orig, "diag", None), "constraint_name", None
        )
        detail = CONSTRAINT_MESSAGES.get(name, "User already exists")
        raise HTTPException(status.HTTP_409_CONFLICT, detail) from exc

    await session.refresh(db_user)
    return {
        "id": db_user.id,
        "username": db_user.username,
        "email": db_user.email,
    }
