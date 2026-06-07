from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db
from core.security import hash_password
from users.models import User
from users.schemas import RegisterUserRequest

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def read_users(session: AsyncSession = Depends(db.session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return {
        "users": [
            {"id": u.id, "username": u.username, "email": u.email}
            for u in users
        ]
    }

@router.post("/")
async def create_user(user: RegisterUserRequest, session: AsyncSession = Depends(db.session)):
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password),
    )
    session.add(db_user)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        constraint = getattr(getattr(exc.orig, "diag", None), "constraint_name", "") or ""
        if "email" in constraint:
            detail = "Email already registered"
        elif "username" in constraint:
            detail = "Username already taken"
        else:
            detail = "User already exists"
        raise HTTPException(status.HTTP_409_CONFLICT, detail=detail) from exc

    await session.refresh(db_user)
    return {
        "id": db_user.id,
        "username": db_user.username,
        "email": db_user.email,
    }