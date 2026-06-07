---
name: add-setting
description: Add or change a configuration value in the pydantic-settings ApiSettings class. Use when the user wants a new env-driven config value, secret, or to adjust settings loading in core/settings.py.
---

# Add a configuration setting

Config lives in `core/settings.py` as `ApiSettings(BaseSettings)`. Values are loaded from
environment variables and the `.env` file, with the `API_` prefix stripped via `env_prefix="API_"`.

## How the prefix works

`env_prefix="API_"` means a field named `KEY` is populated from the env var `API_KEY`.
Existing fields: `API_KEY`, `API_SECRET` (field names `API_KEY`/`API_SECRET` → env `API_API_KEY`?).

> Note: the current field names include the prefix (`API_KEY`), so with `env_prefix="API_"`
> they actually read from `API_API_KEY`. When adding fields, follow the prefix rule consistently —
> name the field WITHOUT the `API_` prefix (e.g. `TIMEOUT`) so it reads from `API_TIMEOUT`.

## Steps

1. Add a typed field to `ApiSettings`:
   ```python
   class ApiSettings(BaseSettings):
       API_KEY: str
       API_SECRET: str
       TIMEOUT: int = 30          # reads API_TIMEOUT, default 30
       DEBUG: bool = False        # reads API_DEBUG
   ```
2. Give it a type hint; add a default only if the value is optional.
3. Add the corresponding `API_`-prefixed entry to `.env` (and document it in `README.md` if relevant).
4. Use the settings via an instance: `settings = ApiSettings()`. Consider a cached accessor:
   ```python
   from functools import lru_cache

   @lru_cache
   def get_settings() -> ApiSettings:
       return ApiSettings()
   ```
   and inject it in routes with `Depends(get_settings)`.

## Notes

- `extra="ignore"` means unknown env vars won't raise.
- Required fields (no default) will fail at startup if missing from env/`.env` — that's intentional.
- Never commit real secrets; `.env` should stay out of version control.
