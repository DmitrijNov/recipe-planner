---
name: add-endpoint
description: Add a new FastAPI endpoint (route) to the cookbook app following project conventions. Use when the user asks to add, create, or expose a new API route/endpoint/handler.
---

# Add a FastAPI endpoint

Add HTTP endpoints to the cookbook app. The app lives in `core/main.py` as `app = FastAPI()`.

## Conventions

- Handlers are `async def`.
- Use a typed Pydantic model for request/response bodies — never raw dicts for non-trivial payloads.
- Return Pydantic models or plain dicts; FastAPI serializes them.
- Use FastAPI status codes from `fastapi.status` (e.g. `status.HTTP_201_CREATED`).
- Validate path/query params with type hints; use `Annotated[..., Query(...)]` / `Path(...)` for constraints.

## When the app grows beyond a couple of routes

Move routes into an `APIRouter` instead of piling them onto `app`:

```python
# core/routers/items.py
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/items", tags=["items"])


class Item(BaseModel):
    id: int
    name: str


@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: int) -> Item:
    return Item(id=item_id, name="example")
```

Then wire it up in `core/main.py`:

```python
from core.routers import items

app.include_router(items.router)
```

## Steps

1. Decide whether the route belongs on `app` (small app) or a new `APIRouter` module under `core/routers/`.
2. Define request/response Pydantic models.
3. Implement the `async def` handler with full type hints and an explicit `response_model`/return type.
4. If you created a new router, `include_router` it in `core/main.py`.
5. Verify with the dev server (see the `run-dev` skill) and check `http://127.0.0.1:8000/docs`.
