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

# View logs for a specific container
docker compose logs app
docker compose logs db

# Follow logs in real time
docker compose logs -f app

# List running containers
docker ps
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

```bash
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
DATABASE_URL=postgresql://user:password@localhost:5432/interview_prep uv run python -m app.seeds.seed
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
DATABASE_URL=postgresql://user:password@localhost:5432/interview_prep uv run uvicorn app.main:app --reload
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
