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

## Architecture decisions

Non-trivial decisions get an [ADR](docs/adr/) before implementation. Use the ADR issue template to draft the decision, then commit the markdown file under `docs/adr/NNNN-slug.md`.

---

## Reporting issues

- **Bugs** — use the bug issue template.
- **Features / tasks** — use the task issue template.
- **Security vulnerabilities** — see [SECURITY.md](SECURITY.md). Do not file public issues for security bugs.
