import datetime
from uuid import uuid4

import jwt
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from auth.schemas import LoginUserSchema, RegisterReqSchema, TokenResponse
from auth.security.passwords import hash_password, verify_password
from core.settings import api_settings
from users.models import User

ALGORITHM = "HS256"


class TokenService:
    access_ttl_minutes = 15
    refresh_ttl_days = 7

    @classmethod
    def create_access_token(cls, user: User) -> str:
        expire = datetime.datetime.now(tz=datetime.UTC) + datetime.timedelta(
            minutes=cls.access_ttl_minutes
        )
        to_encode = {
            "sub": user.username,
            "type": "access",
            "jti": str(uuid4()),
            "exp": expire,
        }
        encoded_jwt = jwt.encode(
            to_encode, api_settings.JWT_SECRET, algorithm=ALGORITHM
        )
        return encoded_jwt

    @classmethod
    def create_refresh_token(cls, user: User) -> str:
        expire = datetime.datetime.now(tz=datetime.UTC) + datetime.timedelta(
            days=cls.refresh_ttl_days
        )
        to_encode = {
            "sub": user.username,
            "type": "refresh",
            "jti": str(uuid4()),
            "exp": expire,
        }
        encoded_jwt = jwt.encode(
            to_encode, api_settings.JWT_SECRET, algorithm=ALGORITHM
        )
        return encoded_jwt

    @classmethod
    def create_token_pair(cls, user: User) -> TokenResponse:
        return TokenResponse(
            access_token=cls.create_access_token(user),
            refresh_token=cls.create_refresh_token(user),
        )


class AuthService:
    def __init__(self, token_service):
        self.token_service = TokenService()

    async def authenticate(
        self, login_data: LoginUserSchema, session: AsyncSession
    ) -> TokenResponse | bool:
        user = await session.scalar(
            select(User).where(User.username == login_data.username)
        )
        if not user:
            return False
        if not verify_password(login_data.password, user.password_hash):
            return False
        return self.token_service.create_token_pair(user)

    async def refresh(
        self, refresh_token: str, session: AsyncSession
    ) -> TokenResponse | bool:
        try:
            payload = jwt.decode(
                refresh_token, api_settings.JWT_SECRET, algorithms=[ALGORITHM]
            )
        except jwt.InvalidTokenError:
            return False

        if payload.get("type") != "refresh":
            return False

        username = payload.get("sub")
        if not username:
            return False

        user = await session.scalar(select(User).where(User.username == username))
        if not user:
            return False

        return self.token_service.create_token_pair(user)

    async def register(
        self, user_data: RegisterReqSchema, session: AsyncSession
    ) -> TokenResponse | bool:
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=hash_password(user_data.password),
            created_at=datetime.datetime.now(tz=datetime.UTC),
        )
        session.add(db_user)

        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()
            return False

        await session.refresh(db_user)
        return self.token_service.create_token_pair(db_user)
