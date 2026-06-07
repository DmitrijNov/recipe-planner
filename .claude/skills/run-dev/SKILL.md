---
name: run-dev
description: Run, restart, or debug the FastAPI cookbook dev server and inspect its endpoints. Use when the user wants to start the app, hit an endpoint, check the OpenAPI docs, or troubleshoot startup errors.
---

# Run the dev server

Dependencies are managed with **uv**. Always prefix commands with `uv run`.

## Commands

```bash
uv sync                          # install/refresh dependencies
uv run fastapi dev core/main.py  # dev server, auto-reload, binds 127.0.0.1:8000
uv run python -m core.main       # run via uvicorn directly, binds 0.0.0.0:8000
```

- Prefer `fastapi dev` while developing — it auto-reloads on file changes.
- The app object is `core.main:app` (also declared under `[tool.fastapi]` in `pyproject.toml`).

## Verify it's up

```bash
curl -s http://127.0.0.1:8000/        # -> {"message":"pong"}
```

- Interactive docs: http://127.0.0.1:8000/docs (Swagger UI)
- OpenAPI schema: http://127.0.0.1:8000/openapi.json

## Running in the background

When you need the server up while you test against it, start it as a background process,
poll the root endpoint until it responds, then run your checks. Stop it when done.

## Troubleshooting

- **`ValidationError` on startup** → a required `ApiSettings` field is missing from the
  environment / `.env`. See the `add-setting` skill for field/env-var naming.
- **`ModuleNotFoundError`** → run `uv sync`, and invoke through `uv run` (not bare `python`).
- **Port already in use** → another instance is running; find and stop it before restarting.
