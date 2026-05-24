# PrepVault Roadmap

PrepVault is a software engineering interview prep platform — study guides, a coding playground with real code execution, and (later) AI-assisted practice and employer matching.

This roadmap documents the path from the current state to a production-grade, publicly deployed system. It is built incrementally — each phase ships as a coherent set of pull requests, with architecture decisions captured in [`docs/adr/`](docs/adr/).

> Note: this roadmap reflects intent, not a fixed contract. Scope and ordering may shift as the project evolves. Tracked execution lives on the [GitHub Project board](https://github.com/users/dimitrijekastratovic/projects/2).

---

## Status

| Phase | Status |
|---|---|
| 1 — Study UI (sidebar + markdown content) | ✅ Complete |
| 2 — Landing page, syntax highlighting, Docker Compose | ✅ Complete |
| 3 — Authentication (bcrypt + JWT) | ✅ Complete |
| 4 — Auth frontend + UI polish | ✅ Complete |
| 5 — Coding playground scaffolding (React + Monaco) | ✅ Complete |
| **5.6 — Judge0 integration** | 🚧 In progress |
| 5.7 — Polish & hardening | ⏳ Next |
| 5.8 — Production CI/CD + deployment | ⏳ Planned |
| Next.js migration (when going public) | 🔮 Later |
| 6 — AI assistant | 🔮 Later |
| 7 — Progress tracking, mock interviews, employer matching | 🔮 Later |

---

## Phase 5.6 — Judge0 Integration

Submit user code from the playground and return a verdict (AC / WA / TLE / RE / CE). Built with a service abstraction so the execution provider can be swapped without touching business logic.

**Outcomes:**
- Self-hosted Judge0 in Docker Compose
- `CodeExecutionService` interface with Judge0 implementation
- `Submission` model + endpoints under `/api/v1/`
- Alembic introduced for database migrations
- WebSocket-based real-time verdict delivery
- ADR documenting the code execution choice

---

## Phase 5.7 — Polish & Hardening

The largest phase. Goal: take a working app to a senior-engineer-quality codebase. Each sub-phase ships as its own set of PRs.

### A. Clean architecture
- Service layer between routers and DB
- Repository pattern for data access
- ADR documenting layering choices

### B. Testing pyramid
- Unit tests for service layer (no I/O)
- Integration tests for routers + DB
- End-to-end tests via Playwright (auth flow, submission flow)
- Contract tests for Judge0
- Load tests via k6 or Locust
- Coverage reporting in CI

### C. Database & performance
- Indexes on foreign keys and hot query columns
- N+1 query audit
- Pagination on list endpoints

### D. Auth hardening
- Email verification on registration (real provider, abstracted)
- Password reset flow
- Rate limiting on auth and submission endpoints
- Audit logging for auth events

### E. API design
- All routes migrated to `/api/v1/`
- Consistent error response shape across endpoints
- OpenAPI documentation cleanup

### F. Observability
- Structured JSON logging with request ID propagation
- Sentry integration for error tracking
- Prometheus metrics (request latency, error rate, Judge0 latency)
- `/health` and `/ready` endpoints
- Grafana dashboard

### G. Security & resilience
- OWASP top 10 audit with documented mitigations
- Secure cookies, HSTS in production
- Graceful shutdown handler (SIGTERM)
- Secrets management strategy

### H. Process & docs
- README rewrite with architecture diagram
- CONTRIBUTING.md
- Pre-commit hooks (ruff, mypy)
- All ADRs reviewed and indexed

---

## Phase 5.8 — Production CI/CD & Deployment

Take the hardened app live with a real CD pipeline and monitoring.

**Outcomes:**
- Hosting provider chosen and documented in an ADR
- Multi-stage Dockerfile with image scanning
- Full test pyramid running in CI with coverage threshold
- CD on `main` merge with blue/green or canary rollout
- Production secrets manager
- HTTPS + custom domain
- Production Sentry, metrics, and dashboards
- Backup strategy for production database

---

## Content Quality (ongoing, parallel to all phases)

The platform's value depends on the quality of its content as much as its engineering. Content work runs in parallel to feature development:

**Study guides:**
- Audit existing articles for correctness, depth, and clarity
- Expand Data Structures and Algorithms coverage (currently partial)
- Build out System Design (currently a single article)
- Add CS Fundamentals (OS, networking, databases, concurrency)
- Add Behavioral interview prep (STAR method, common questions, frameworks)
- Establish a content style guide for consistency

**Coding problems:**
- Expand from current 5 seed problems to a curated set covering common interview patterns (~50-100 problems)
- Each problem: clear description, edge-case-covering test cases, runtime/memory limits validated
- Tag by topic and difficulty
- Include reference solutions (visible after attempt) with complexity analysis

**Review process:**
- All content reviewed against authoritative sources (CLRS, Designing Data-Intensive Applications, official docs) before publish
- ADR for content review and contribution workflow when relevant

**Concrete starting tickets:**
- Audit existing Data Structures articles for correctness and depth
- Audit existing Algorithms articles for correctness and depth
- Establish content style guide (`content/STYLE.md`)
- Outline System Design curriculum (10 core articles) and draft first 3
- Outline CS Fundamentals curriculum
- Outline Behavioral interview prep curriculum
- Add 10 curated coding problems covering core patterns
- Add reference solutions (with complexity analysis) to existing problems

---

## Frontend Migration to Next.js (when going public)

The current frontend is intentionally split:
- Study UI and auth pages: server-rendered HTML + vanilla JS (FastAPI templates)
- Playground: React (Vite) — chosen for interactivity, not SEO

When PrepVault opens to the public, SEO and performance matter — study guide pages need to be indexable and load fast. At that point the frontend migrates to **Next.js**:

- Server-side rendering for study guides (SEO + performance)
- File-based routing replaces the current split between FastAPI templates and React SPA
- API routes for any frontend-only concerns; FastAPI remains the backend
- Migration leverages the clean, modular React already built — components transfer mostly as-is
- ADR documenting the migration trigger, scope, and trade-offs

This is deliberately deferred — building Next.js before the product is real would be premature optimization. The decision to migrate is gated on going public.

---

## Phase 6 — AI Assistant

Chat drawer integrated into study and playground pages. Designed but not yet planned in detail.

---

## Phase 7 — Advanced features

Progress tracking, adaptive difficulty, mock interview mode, employer matching, Stripe-backed premium subscriptions.

---

## Engineering principles

PrepVault is also a portfolio project demonstrating production-grade engineering. Every layer is held to standards a senior engineer would expect to see in a real company's codebase:

- Clean abstractions and dependency inversion
- Config-driven design — no hardcoded vendors or URLs
- Full testing pyramid, used appropriately at each layer
- Observability from day one in features that need it
- Migrations, not hand-edited schemas
- API versioning, consistent errors, idempotency where appropriate
- Documented decisions (ADRs) for every non-trivial choice

See [`docs/adr/`](docs/adr/) for the decision log.
