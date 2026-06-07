from contextlib import asynccontextmanager
from logging import getLogger

from fastapi import FastAPI

from core.database import db

logger = getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    try:
        yield
    finally:
        logger.info("shutting down")
        await db.disconnect()
