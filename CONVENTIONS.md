# Conventions

How a feature module is structured and behaves in PrepVault. This is the living detail behind [ADR-0006](docs/adr/0006-feature-module-conventions.md); the *why we standardize* lives there, the *what* lives here.

`app/submissions/` is the reference implementation — when in doubt, match it.

> **Status:** `submissions` follows all of this today. The earlier modules (`auth`, `problems`, `content`) predate it and are being brought into conformance — see #84 (read serialization), #85 (domain exceptions), #86 (status codes). New code conforms from the start.

## Module file layout

A feature lives in one package under `app/<feature>/`. Files are present *when the feature needs them*, not by template:

| File | When present |
|---|---|
| `router.py` | always — the feature's HTTP (or WebSocket) endpoints |
| `schemas.py` | always — request/response models (`*Create`, `*Read`); never expose the table model directly |
| `models.py` | only for features with their own DB tables (`content` is file-based, so it has none) |
| `service.py` | only when there is orchestration or business logic beyond a trivial CRUD call |
| `exceptions.py` | when the feature raises domain errors (see Error handling) |

Shared infrastructure (DB engine, config, auth dependency) lives in `app/core/` and `app/auth/`, never in a top-level technical-layer directory ([ADR-0005](docs/adr/0005-feature-modular-layout.md)).

**Model ownership** follows the owning domain: `auth` owns `User`; other features import it (`from app.auth.models import User`).

## Error handling

Services raise **domain exceptions**; routers translate them to HTTP. The service layer never imports `fastapi`.

- Define domain exceptions in the feature's `exceptions.py`, subclassing a feature base (e.g. `SubmissionError(Exception)`). Carry the offending id/value as an attribute for the message.
- Services raise these and stay transport-agnostic — the same service is callable from a router, a WebSocket handler, or a worker.
- Routers catch domain exceptions and translate to `HTTPException` (per-router `try/except`, keeping the mapping next to the endpoint). WebSocket handlers translate the *same* exceptions to close codes.

Reference: `submissions/service.py` raises `SubmissionNotFound` / `SubmissionForbidden`; `submissions/router.py` maps them to 404/403 and `submissions/websocket.py` maps them to 4404/4403.

## Read serialization

- Convert ORM rows to a `*Read` schema with `Model.model_validate(row)` — not by hand-copying fields.
- Manual construction is only for non-ORM sources (e.g. file-based `content`).
- On read paths that traverse relationships, eager-load them so a list endpoint doesn't fire one query per row (no N+1). Watch for `DetachedInstanceError` when validating outside the session scope.

## Success status codes

Endpoints that **create** a resource declare `status_code=201` on the route decorator (so OpenAPI documents it correctly), even when a replay/idempotent path returns 200. Don't let a creating endpoint silently return the default 200.

## Tests

- **Central `tests/` directory mirroring the feature packages** (`tests/<feature>/`), not test files colocated under `app/<feature>/`. This keeps tests trivially excludable from the shipped Docker image and lets a single top-level harness (`tests/conftest.py`) be shared.
- The test directory is named **plural to match the module** (`submissions` → `tests/submissions/`).
- **Split test files by concern within the feature, mirroring the source**: `test_router.py` (endpoints via `TestClient` + `dependency_overrides`), `test_service.py` (logic with a session + fakes, no HTTP), `test_models.py` (DB/ORM behavior), plus others as the feature needs (e.g. `test_websocket.py`). Rationale: router and model tests don't share dependencies, so they don't share a file. A feature-local `conftest.py` holds its fixtures (`submissions/` is the reference).
- **Test naming:**
  - Endpoint/behavior tests: `test_<subject>_<verb>_<result>_when_<condition>` — e.g. `test_get_submission_returns_403_for_other_user`, `test_websocket_closes_4403_when_submission_belongs_to_other_user`.
  - Pure-function unit tests: `test_<fn>_should_<behavior>` — e.g. `test_map_status_should_translate_status_ids_to_submission_statuses`.
  - Pick the form that matches the kind of test; don't mix them within a kind.
- Test through the public surface with concrete assertions; mock external collaborators (Judge0, etc.) at the edges, not the thing under test.
