# PrepVault

A software engineering interview prep platform — study guides, a coding playground with real code execution, and (planned) AI-assisted practice and employer matching.

> 🚧 **Status:** Active development. Currently in **Phase 5.6 — Judge0 integration**. See [ROADMAP.md](ROADMAP.md) for the full plan.

---

## Overview

PrepVault is being built as a production-grade web application demonstrating the architecture, testing, and operational practices expected of a senior engineering team. The product offers:

- **Study guides** — curated articles on data structures, algorithms, system design, CS fundamentals, and behavioral interview prep, rendered from markdown and reviewed against authoritative sources.
- **Coding playground** — an in-browser code editor (Monaco) backed by a sandboxed execution service. Submissions return verdicts (AC / WA / TLE / RE / CE) with runtime and memory metrics. Curated problem set covering common interview patterns.
- **(Planned) AI assistant** — context-aware chat that can explain problems, hint, or review solutions.
- **(Planned) Employer matching** — two-sided platform connecting strong performers with hiring teams.

---

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12, FastAPI, SQLModel |
| Database | PostgreSQL |
| Migrations | Alembic *(introduced in Phase 5.6)* |
| Frontend (study) | HTML / CSS / vanilla JS |
| Frontend (playground) | React (Vite) + Monaco Editor |
| Code execution | Self-hosted Judge0 *(Phase 5.6)* |
| Real-time | WebSockets *(Phase 5.6)* |
| Containerization | Docker, Docker Compose |
| CI/CD | GitHub Actions, GHCR |
| Observability *(planned)* | Sentry, Prometheus, Grafana |
| Hosting *(planned)* | TBD — ADR pending |

---

## Architecture

```mermaid
graph TB
    Client[Browser<br/>Study UI + Playground]

    subgraph "FastAPI Application"
        Router[HTTP Routers<br/>/api/v1/...]
        WS[WebSocket Handlers]
        Service[Service Layer<br/>Business Logic]
        Repo[Repository Layer<br/>Data Access]
        Auth[Auth<br/>bcrypt + JWT]
    end

    subgraph "Data"
        DB[(PostgreSQL<br/>users, problems,<br/>submissions, content)]
    end

    subgraph "Execution"
        Exec[CodeExecutionService<br/>interface]
        Judge0[Judge0<br/>sandboxed runner]
    end

    Client -->|HTTPS| Router
    Client -.->|WSS| WS
    Router --> Service
    WS --> Service
    Service --> Repo
    Service --> Auth
    Service --> Exec
    Repo --> DB
    Exec -.implements.-> Judge0
```

The `CodeExecutionService` is an abstraction — Judge0 is one implementation. Future implementations (custom sandbox, alternative providers) can be swapped in without changing business logic.

---

## Getting started

### Prerequisites

- Docker + Docker Compose
- Node.js 20+ (for the playground frontend)

### Run the stack

```bash
git clone https://github.com/dimitrijekastratovic/prepvault.git
cd prepvault
cp .env.example .env  # fill in any required secrets
docker compose up --build -d
```

The app is available at [http://localhost:8000](http://localhost:8000).

### Run the playground frontend (dev mode)

```bash
cd playground
npm install
npm run dev
```

The Vite dev server runs on [http://localhost:5173](http://localhost:5173) and proxies `/api` to the FastAPI backend.

### Seed sample problems

```bash
DATABASE_URL=postgresql://user:password@localhost:5432/interview_prep \
  uv run python -m app.seeds.seed
```

See [COMMANDS.md](COMMANDS.md) for the full development cheat sheet.

---

## Project structure

```
prepvault/
├── app/                    # FastAPI application
│   ├── routers/            # HTTP route handlers
│   ├── services/           # Business logic (Phase 5.7)
│   ├── repositories/       # Data access (Phase 5.7)
│   ├── models/             # SQLModel ORM models
│   ├── schemas/            # Pydantic request/response schemas
│   ├── auth/               # bcrypt + JWT utilities
│   └── seeds/              # Seed data and scripts
├── content/                # Markdown study guides
├── static/                 # Study UI (HTML/CSS/JS)
├── templates/              # HTML templates served by FastAPI
├── playground/             # React + Vite playground app
├── tests/                  # pytest suite
├── docs/
│   └── adr/                # Architecture Decision Records
├── docker-compose.yml
├── Dockerfile
├── ROADMAP.md
└── COMMANDS.md
```

---

## Development workflow

- **Branching** — feature branches off `main`, PRs required, CI must pass, squash merge.
- **Tests** — `pytest` for backend, Playwright for end-to-end *(Phase 5.7)*.
- **Linting** — `ruff` for Python; pre-commit hooks planned for Phase 5.7.
- **Migrations** — Alembic *(introduced Phase 5.6)*.
- **Decisions** — every non-trivial architectural choice gets an ADR in [docs/adr/](docs/adr/).

---

## Roadmap

See [ROADMAP.md](ROADMAP.md) for the full phased plan from current state to production deployment.

---

## Engineering principles

PrepVault is also a portfolio project demonstrating production-grade engineering. Every layer is held to standards a senior engineer would expect in a real company's codebase:

- **Clean abstractions** — service-layer pattern, dependency inversion. External providers (code execution, email) accessed through interfaces.
- **Config-driven** — no hardcoded URLs, keys, or feature toggles; everything via environment variables.
- **Testing pyramid** — unit, integration, and end-to-end tests, each used for what it's good at.
- **Observability from day one** — structured logging, error tracking, and metrics for any feature that matters in production.
- **Migrations, not hand-edited schemas** — schema changes go through Alembic, reviewed in PRs.
- **API versioning** — all endpoints under `/api/v1/`, with a consistent error response shape.
- **Documented decisions** — every non-trivial choice captured as an ADR.

See [docs/adr/](docs/adr/) for the decision log.

---

## License

[MIT](LICENSE)
