# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A small FastAPI learning/playground project ("cookbook"). Python 3.13, dependencies managed with **uv** (`uv.lock` present).

## Commands

```bash
uv sync                          # install dependencies
uv sync --all-groups             # install runtime + dev dependencies (ruff, pre-commit)
uv run fastapi dev core/main.py  # run dev server (auto-reload, binds 127.0.0.1:8000)
uv run python -m core.main       # run directly via uvicorn (binds 0.0.0.0:8000)

uv run pre-commit install        # install the git pre-commit hook (one-time)
uv run pre-commit run --all-files # run all hooks against the whole repo
uv run ruff check --fix .        # lint + autofix
uv run ruff format .             # format
```

Linting/formatting is **Ruff** (config in `pyproject.toml` under `[tool.ruff]`), run via **pre-commit** (`.pre-commit-config.yaml`). There are no tests configured yet.

## Structure

- `core/main.py` — FastAPI app entrypoint (`core.main:app`, also declared under `[tool.fastapi]` in `pyproject.toml`).
- `core/settings.py` — pydantic-settings config (`ApiSettings`) loading `API_`-prefixed vars from `.env`.
- `docker/` — empty placeholder package.
