# Hermes Celery worker image.
FROM python:3.12-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml README.md ./
COPY packages/hermes-domain ./packages/hermes-domain
COPY services/worker ./services/worker

RUN uv pip install --system ./packages/hermes-domain ./services/worker

# Healthcheck: ensure the Celery app imports and can inspect its own registry.
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=5 \
    CMD python -c "from hermes_worker.app import app; assert 'hermes.ping' in app.tasks"

CMD ["celery", "-A", "hermes_worker.app", "worker", "--loglevel=info"]
