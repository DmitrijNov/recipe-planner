# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A small FastAPI learning/playground project ("cookbook"). Python 3.13, dependencies managed with **uv** (`uv.lock` present).

## Commands

```bash
uv sync                          # install dependencies
uv run fastapi dev core/main.py  # run dev server (auto-reload, binds 127.0.0.1:8000)
uv run python -m core.main       # run directly via uvicorn (binds 0.0.0.0:8000)
```

There are no tests or linters configured yet.

## Structure

- `core/main.py` — FastAPI app entrypoint (`core.main:app`, also declared under `[tool.fastapi]` in `pyproject.toml`).
- `core/settings.py` — pydantic-settings config (`ApiSettings`) loading `API_`-prefixed vars from `.env`.
- `docker/` — empty placeholder package.