# Dev Commands Cheatsheet

## Docker

```bash
# Build and start all containers in background
docker compose up --build -d

# Start containers without rebuilding (faster, use when code unchanged)
docker compose up -d

# Stop containers (keeps volumes/data intact)
docker compose down

# Stop containers AND delete volumes (wipes DB data — clean slate)
docker compose down -v

# View logs for a specific service
docker compose logs app
docker compose logs app-db
docker compose logs judge0-api
docker compose logs judge0-worker
docker compose logs judge0-db
docker compose logs judge0-redis

# Follow logs in real time
docker compose logs -f app

# List running containers (with health status)
docker compose ps
```

## Judge0 smoke tests

```bash
# Replace TOKEN with the value of JUDGE0_AUTH_TOKEN in .env / AUTHN_TOKEN in judge0.env.

# Verify Judge0 API is reachable and auth is wired
curl -H "X-Auth-Token: TOKEN" http://localhost:2358/about

# List supported languages
curl -H "X-Auth-Token: TOKEN" http://localhost:2358/languages

# Submit a trivial Python program end-to-end (language_id 71 = Python 3.8.1)
curl -X POST 'http://localhost:2358/submissions?wait=true&base64_encoded=false' \
  -H "Content-Type: application/json" \
  -H "X-Auth-Token: TOKEN" \
  -d '{"source_code":"print(\"hello\")","language_id":71}'
```

## Dependencies (uv)

PrepVault uses [uv](https://docs.astral.sh/uv/) for Python dependency management — see [ADR-0002](docs/adr/0002-dependency-management-with-uv.md).

```bash
# Install all deps (runtime + dev) into .venv from uv.lock
uv sync

# Install runtime deps only (what production / Docker does)
uv sync --no-dev

# Add a runtime dependency
uv add fastapi

# Add a dev dependency
uv add --dev pytest

# Refresh the lockfile to newest compatible versions
uv lock --upgrade

# Run any command inside the project venv (no manual activation needed)
uv run <cmd>
```

## Tests

Tests run against a real Postgres instance (the `prepvault_test` database created
on first boot by `docker/app-db-init/01-create-test-db.sql`). The `app-db`
container must be running; pytest connects via the published 5432 port on
localhost.

First-time setup:

```bash
cp .env.test.example .env.test
# Edit .env.test and fill in TEST_DATABASE_URL with the credentials from
# app-db.env (host stays as localhost — pytest runs on the host, not in compose).
```

`.env.test` is auto-loaded by pytest-dotenv on startup — no `export` needed.

```bash
# Make sure the database container is up
docker compose up -d app-db

# Run all tests
uv run pytest

# Run a specific test file
uv run pytest tests/test_auth.py

# Run with verbose output
uv run pytest -v

# Run a specific test by name
uv run pytest -k "test_login"
```

## Seeding the Database

```bash
# Run seed script (DB container must be running, app container not required)
DATABASE_URL=postgresql://app_admin_user:app_admin_password123@localhost:5432/prepvault_db uv run python -m app.seeds.seed
```

## Linting

```bash
# Run ruff linter
uv run ruff check .

# Auto-fix lint issues
uv run ruff check . --fix
```

## Local Dev (without Docker)

```bash
# First-time setup: install uv, then sync deps
brew install uv     # macOS; see uv docs for other platforms
uv sync

# Run FastAPI app locally (DB must be running via Docker)
DATABASE_URL=postgresql://app_admin_user:app_admin_password123@localhost:5432/prepvault_db uv run uvicorn app.main:app --reload
```

## Git

```bash
# Create and switch to a new branch
git checkout -b feature/branch-name

# Stage specific files
git add app/routers/problems.py

# Commit
git commit -m "your message"

# Push branch and set upstream
git push -u origin feature/branch-name
```
