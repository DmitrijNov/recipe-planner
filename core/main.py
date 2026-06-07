import logging

import uvicorn
from fastapi import FastAPI

from core.lifespan import lifespan
from users.route import router as users_router

logging.basicConfig(level=logging.INFO)


app = FastAPI(
    lifespan=lifespan,
    docs_url="/swagger",
)


@app.get("/")
async def ping():
    return {"message": "pong"}


app.router.include_router(users_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
