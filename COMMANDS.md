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

## Tests

```bash
# Run all tests
.venv/bin/python3 -m pytest

# Run a specific test file
.venv/bin/python3 -m pytest tests/test_auth.py

# Run with verbose output
.venv/bin/python3 -m pytest -v

# Run a specific test by name
.venv/bin/python3 -m pytest -k "test_login"
```

## Seeding the Database

```bash
# Run seed script (DB container must be running, app container not required)
DATABASE_URL=postgresql://user:password@localhost:5432/interview_prep .venv/bin/python3 -m app.seeds.seed
```

## Linting

```bash
# Run ruff linter
.venv/bin/python3 -m ruff check .

# Auto-fix lint issues
.venv/bin/python3 -m ruff check . --fix
```

## Local Dev (without Docker)

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run FastAPI app locally (DB must be running via Docker)
DATABASE_URL=postgresql://user:password@localhost:5432/interview_prep .venv/bin/uvicorn app.main:app --reload
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
