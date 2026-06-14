import logging

import uvicorn
from fastapi import FastAPI

from auth.router import auth_router
from core import middlewares
from core.lifespan import lifespan
from recipes.router import router as recipe_router
from users.route import router as users_router

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    lifespan=lifespan,
    docs_url="/swagger",
)


@app.get("/")
async def ping():
    return {"message": "pong"}


app.middleware("http")(middlewares.custom_middleware)
app.router.include_router(auth_router)
app.router.include_router(users_router)
app.router.include_router(recipe_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
