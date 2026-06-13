from fastapi import APIRouter, Depends, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.security.tokens import require_bearer_token
from core.database import db
from users.models import User

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(require_bearer_token)],
)


@router.get("/")
async def read_users(session: AsyncSession = Depends(db.session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return {
        "users": [{"id": u.id, "username": u.username, "email": u.email} for u in users]
    }


async def get_current_user(
    request: Request, session: AsyncSession = Depends(db.session)
) -> None:
    user = await session.execute(select(User).limit(1))
    return user.scalar_one()
