# Cookbook

An AI-powered meal planning API. The goal is an app that **plans meals using AI agents** — _the agent layer is still TBD_; what exists today is the FastAPI backend (users, auth primitives, async Postgres) that it will be built on.

Small FastAPI learning/playground project. Python 3.13, dependencies managed with [uv](https://docs.astral.sh/uv/).

## Status

> ⚠️ Early WIP. The meal-planning AI agents are **not implemented yet** (TBD). Current functionality is limited to user registration/listing and the supporting infrastructure.

**Implemented**
- FastAPI app with async lifespan-managed Postgres connection (SQLAlchemy 2.0 async + psycopg3)
- User model + register/list endpoints
- Argon2 password hashing (`pwdlib`)
- Pydantic-settings config, Alembic migrations
- Ruff linting/formatting via pre-commit + GitHub Actions

**Planned (TBD)**
- AI agents that generate meal plans
- Recipe / ingredient / pantry models
- Authentication (login, sessions/tokens) — hashing helpers exist, the flow does not

## Tech stack

| Concern | Choice |
|---|---|
| Web framework | FastAPI |
| ASGI server | uvicorn |
| ORM | SQLAlchemy 2.0 (async) |
| Database | PostgreSQL (via psycopg3) |
| Migrations | Alembic |
| Password hashing | pwdlib (Argon2) |
| Config | pydantic-settings |
| Tooling | uv, Ruff, pre-commit |

## Getting started

### Prerequisites
- Python 3.13
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- A running PostgreSQL instance

### Setup

```bash
# 1. Install dependencies
uv sync                 # runtime only
uv sync --all-groups    # runtime + dev tools (ruff, pre-commit)

# 2. Configure environment
cp .env.example .env    # then edit values

# 3. Apply database migrations
uv run alembic upgrade head

# 4. (optional) install the git pre-commit hook
uv run pre-commit install
```

### Run

```bash
uv run fastapi dev core/main.py   # dev server, auto-reload, 127.0.0.1:8000
uv run python -m core.main        # run via uvicorn, 0.0.0.0:8000
```

Interactive API docs (Swagger UI) are served at **http://127.0.0.1:8000/swagger**.

## Configuration

Environment variables are loaded from `.env` (see `.env.example`).

| Variable | Purpose | Default |
|---|---|---|
| `API_KEY` | App API key (`core.settings.ApiSettings`, prefix `API_`) | — (required) |
| `API_SECRET` | App secret | — (required) |
| `POSTGRES_USER` | DB user | `postgres` |
| `POSTGRES_PASSWORD` | DB password | `postgres` |
| `POSTGRES_DB` | DB name | `cookbook` |
| `POSTGRES_HOST` | DB host | `localhost` |
| `POSTGRES_PORT` | DB port | `5432` |

## API

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Health check — returns `{"message": "pong"}` |
| `GET` | `/users/` | List all users |
| `POST` | `/users/` | Register a user (`username`, `email`, `password`, `confirm_password`) |
| `GET` | `/swagger` | Swagger UI |

## Project structure

```
core/
  main.py        # FastAPI app entrypoint (core.main:app)
  settings.py    # pydantic-settings: ApiSettings + DatabaseSettings
  database.py    # async engine/session factory + declarative Base
  lifespan.py    # connects/disconnects the DB on app startup/shutdown
  security.py    # Argon2 password hashing helpers
  middlewares.py
users/
  models.py      # User SQLAlchemy model
  schemas.py     # Pydantic request models
  route.py       # /users router
migrations/      # Alembic migrations (config in alembic.ini)
docker/          # placeholder
```

## Development

```bash
uv run ruff check --fix .          # lint + autofix
uv run ruff format .               # format
uv run pre-commit run --all-files  # run all hooks
```

Linting and formatting use **Ruff** (config in `pyproject.toml`), enforced locally via pre-commit and in CI via `.github/workflows/lint.yml` on every pull request. There are no tests yet.
