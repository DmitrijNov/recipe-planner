from contextlib import asynccontextmanager

from fastapi import FastAPI
from logging import getLogger
from core.database import db

logger = getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
	await db.connect()
	try:
		yield
	finally:
		logger.info('shutting down')
		await db.disconnect()

