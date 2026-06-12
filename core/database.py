from collections.abc import AsyncIterator
from logging import getLogger

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from core.settings import db_settings

logger = getLogger(__name__)


class Base(DeclarativeBase):
    """Declarative base; all models inherit from this so Alembic can
    discover their metadata for autogenerate."""


class Database:
    """Owns the async engine and session factory for the app's lifetime."""

    def __init__(self) -> None:
        self.engine: AsyncEngine | None = None
        self.session_factory: async_sessionmaker[AsyncSession] | None = None

    async def connect(self) -> None:
        logger.info("creating connection pools")
        self.engine = create_async_engine(
            db_settings.url, pool_pre_ping=True, pool_size=10, max_overflow=2
        )
        self.session_factory = async_sessionmaker(self.engine, expire_on_commit=False)

    async def disconnect(self) -> None:
        logger.info("closing connection pools")
        if self.engine is not None:
            await self.engine.dispose()
            self.engine = None
            self.session_factory = None

    async def session(self) -> AsyncIterator[AsyncSession]:
        """FastAPI dependency yielding a session: `Depends(db.session)`."""
        if self.session_factory is None:
            raise RuntimeError("Database is not connected")
        async with self.session_factory() as session:
            yield session


db = Database()
