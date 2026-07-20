# Hermes API image. Uses uv for fast, reproducible installs.
FROM python:3.12-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Install uv (static binary).
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy the workspace metadata and the packages the API depends on.
COPY pyproject.toml README.md ./
COPY packages/hermes-domain ./packages/hermes-domain
COPY services/api ./services/api

# Install the API package (and its workspace dependency) into a venv.
RUN uv pip install --system ./packages/hermes-domain ./services/api

EXPOSE 8000

# Container-level healthcheck hitting the app's /health endpoint.
HEALTHCHECK --interval=15s --timeout=5s --start-period=20s --retries=5 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8000/health').status==200 else 1)"

CMD ["uvicorn", "hermes_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
