# Contributing to PrepVault

Thanks for your interest in PrepVault. This document covers the practical workflow for contributing — branching, commits, tests, and PRs.

> PrepVault is primarily a portfolio project for the maintainer, but contributions, suggestions, and issues are welcome.

---

## Getting set up

See the [Getting started](README.md#getting-started) section of the README for the full local setup.

Quick version:

```bash
git clone https://github.com/dimitrijekastratovic/prepvault.git
cd prepvault
cp .env.example .env
cp app-db.env.example app-db.env
cp judge0-db.env.example judge0-db.env
cp judge0.env.example judge0.env
cp .env.test.example .env.test
# Fill in real secrets in each file. Comments call out values that must match
# across paired files (e.g. DATABASE_URL ↔ app-db.env, JUDGE0_AUTH_TOKEN ↔ judge0.env,
# TEST_DATABASE_URL ↔ app-db.env credentials).
docker compose up --build -d
```

---

## Branching

- Branch off `main`.
- Use a short, descriptive branch name: `feature/<short-name>`, `fix/<short-name>`, `chore/<short-name>`, `docs/<short-name>`.
- One logical change per branch. If you're tempted to bundle unrelated work, split into separate branches.

## Commits

- Write commits as imperative, present tense: *"Add submission endpoint"*, not *"Added submission endpoint"*.
- Keep the subject line under 72 characters.
- Body (optional) explains the *why*, not the *what* — the diff already shows the what.

## Pull requests

- Use the [PR template](.github/PULL_REQUEST_TEMPLATE.md) — it's applied automatically.
- Link the issue the PR closes (`Closes #N`).
- Every PR must:
  - Pass CI (ruff, pytest, docker build)
  - Be squash-merged (the only merge method allowed on `main`)
  - Have all review conversations resolved
- Keep PRs small. Reviewable in 15 minutes is a good target.

---

## Python dependencies

PrepVault uses [`uv`](https://docs.astral.sh/uv/) for Python dependency management — see [ADR-0002](docs/adr/0002-dependency-management-with-uv.md).

Install uv once: `brew install uv` (macOS) or follow the [official install guide](https://docs.astral.sh/uv/getting-started/installation/).

Common commands:

```bash
uv sync                 # install all deps (runtime + dev) into .venv
uv sync --no-dev        # runtime deps only (what production does)
uv add <pkg>            # add a runtime dependency
uv add --dev <pkg>      # add a dev dependency
uv run <cmd>            # run a command inside the project venv
uv lock --upgrade       # refresh uv.lock to newest compatible versions
```

`pyproject.toml` declares direct deps; `uv.lock` pins the full resolved graph. Both are committed. Don't edit `uv.lock` by hand.

## Running tests

Tests run against a real Postgres instance — same engine as production. The
`app-db` container must be up; pytest connects to the `prepvault_test` database
on `localhost:5432`. Credentials come from `.env.test` (auto-loaded by
pytest-dotenv).

```bash
docker compose up -d app-db   # if not already running
uv run pytest                 # backend tests
uv run ruff check .           # linting
```

End-to-end and frontend tests are planned for Phase 5.7 — see [ROADMAP.md](ROADMAP.md).

---

## Database migrations

The schema is managed with [Alembic](https://alembic.sqlalchemy.org/). The app
does **not** create tables on startup — schema changes are applied out-of-band
by running `alembic upgrade head`. (Startup `create_all` was deliberately
removed: in a multi-replica deployment sharing one database, every replica would
race to build the schema. Migrations are a single, explicit, ordered step
instead.) The command reference lives in
[COMMANDS.md](COMMANDS.md#database-migrations-alembic).

When you change a model, the workflow is:

1. **Edit the model** under the relevant feature package (e.g. `app/submissions/models.py`).
2. **Register it** in `app/core/models_registry.py` if it's a new model. Both
   Alembic's `env.py` and the test harness import this module so
   `SQLModel.metadata` is fully populated — a model that isn't imported here is
   invisible to autogenerate and will be silently skipped.
3. **Autogenerate a migration**: `alembic revision --autogenerate -m "..."`.
4. **Read the generated file by hand.** Autogenerate is a *hint, not a
   contract.* It infers intent from a metadata diff and regularly gets things
   wrong or incomplete. Never commit a migration you haven't read.
5. **Apply it**: `alembic upgrade head`, then confirm the result (`\d <table>`
   in psql, or `alembic upgrade head --sql` to inspect the raw DDL).
6. **Verify it round-trips**: `alembic downgrade -1` then `alembic upgrade head`
   should both succeed and leave no orphaned objects.

### Things autogenerate gets wrong

- **Native PostgreSQL enums.** Autogenerate does not emit the `CREATE TYPE` /
  `DROP TYPE` for a native enum, and it does not make the enum reusable across
  up/down runs. You must hand-edit the migration to create and drop the type
  explicitly. Note that `create_type=False` only works on `postgresql.ENUM`, not
  on `sa.Enum` — using the wrong one leaves orphaned types that break a
  re-`upgrade` after a `downgrade`.
- **`server_default` and other column defaults** are frequently missed or
  rendered as plain Python values — verify they appear in the DDL.
- **Index predicates** (e.g. partial unique indexes with a `WHERE` clause) may
  not be reproduced faithfully — check them against the model.

---

## Architecture decisions

Non-trivial decisions get an [ADR](docs/adr/) before implementation. Use the ADR issue template to draft the decision, then commit the markdown file under `docs/adr/NNNN-slug.md`.

## Feature-module conventions

How a feature module is structured (files, error handling, read serialization, status codes, test layout) is documented in [CONVENTIONS.md](CONVENTIONS.md). Match `app/submissions/` — the reference module — when adding or changing a feature.

---

## Reporting issues

- **Bugs** — use the bug issue template.
- **Features / tasks** — use the task issue template.
- **Security vulnerabilities** — see [SECURITY.md](SECURITY.md). Do not file public issues for security bugs.
