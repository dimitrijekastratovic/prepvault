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

## Running tests

```bash
# Backend tests
pytest

# Linting
ruff check .
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
