FROM docker.io/library/python:3.13-slim-bookworm AS builder

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl

COPY --from=ghcr.io/astral-sh/uv:0.6.13 /uv /uvx /usr/local/bin/

ENV PATH="/.venv/bin:$PATH" \
    UV_PROJECT_ENVIRONMENT="/.venv" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --link-mode=copy

COPY src/ ./src/

RUN uv pip install --no-deps --editable .

FROM docker.io/library/python:3.13-slim-bookworm

COPY --from=builder /.venv /.venv
COPY --from=builder /app /app

ENV PATH="/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

CMD [ ... ]
