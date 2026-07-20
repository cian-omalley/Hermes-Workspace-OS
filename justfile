# Hermes Workspace OS — developer command surface.
# Run `just` to list commands. See docs/PROJECT_BIBLE/10_Claude_Code/Build_Process.md.

set shell := ["bash", "-cu"]

# List available commands (default).
default:
    @just --list

# ---- Environment ----

# Copy the example env file into place (won't overwrite an existing .env).
env:
    @test -f .env || cp config/.env.example .env && echo ".env ready"

# ---- Local stack ----

# Bring up the full local stack (datastores + services).
up:
    docker compose -f infrastructure/compose/docker-compose.yml up -d

# Stop the stack.
down:
    docker compose -f infrastructure/compose/docker-compose.yml down

# Tail stack logs.
logs:
    docker compose -f infrastructure/compose/docker-compose.yml logs -f

# ---- Python (uv) ----

# Install Python workspace dependencies.
py-install:
    uv sync

# Run the API in development.
api:
    uv run --package hermes-api uvicorn hermes_api.main:app --reload --host 0.0.0.0 --port 8000

# Apply database migrations (upgrade to head).
migrate:
    uv run alembic -c database/alembic.ini upgrade head

# Create a new migration (usage: just makemigration "message").
makemigration message:
    uv run alembic -c database/alembic.ini revision -m "{{message}}"

# Seed example data for local development (run after `just migrate`).
seed:
    uv run python scripts/seed.py

# Regenerate the OpenAPI document and the TypeScript client (the contract seam).
gen-client:
    uv run python scripts/dump_openapi.py
    pnpm --filter @hermes/ts-client generate

# Run a Celery worker.
worker:
    uv run --package hermes-worker celery -A hermes_worker.app worker --loglevel=info

# ---- Frontend (pnpm) ----

# Install JS workspace dependencies.
web-install:
    pnpm install

# Run the web app in development.
web:
    pnpm --filter @hermes/web dev

# ---- Quality gates ----

# Lint + format-check + type-check across Python and TS.
check:
    uv run ruff check .
    uv run ruff format --check .
    uv run mypy packages services
    pnpm --filter @hermes/web lint
    pnpm --filter @hermes/web typecheck

# Auto-fix formatting.
fmt:
    uv run ruff check --fix .
    uv run ruff format .

# Run unit + integration tests (Python + TS).
test:
    uv run pytest
    pnpm --filter @hermes/web test

# Run end-to-end smoke tests (requires the stack to be up).
e2e:
    uv run pytest tests/smoke -m smoke
