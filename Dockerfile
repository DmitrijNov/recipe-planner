FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	UV_PYTHON_PREFERENCE=only-system

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock README.md /app/
RUN uv sync --frozen --no-dev --python 3.14

COPY . /app

EXPOSE 8000

CMD ["uv", "run", "--no-sync", "python", "-m", "core.main"]
