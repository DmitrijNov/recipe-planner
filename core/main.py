from fastapi import FastAPI
import uvicorn
from core.middlewares import add_header
from core.lifespan import lifespan
import logging
from users.route import router as users_router


logging.basicConfig(level=logging.INFO)


app = FastAPI(
    lifespan=lifespan,
    docs_url="/swagger",
)

app.middleware("http")(add_header)


@app.get("/")
async def ping():
    return {"message": "pong"}


# Include the users router
app.include_router(users_router)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)