# ADR-0005: Feature-modular application layout

**Date:** 2026-06-09

## Context

`app/` was drifting toward a layered layout — top-level `models/`, `routers/`, `schemas/` directories, each holding one file per feature. Understanding a single capability (say, "problems") meant hopping across three or four sibling directories to assemble the full picture. That navigation cost was the concrete trigger: as features multiply, each technical-layer directory grows into a pile of unrelated files, and the parts that actually change together drift apart.

We needed to decide how to organize `app/` before more features (submissions, and beyond) compounded the problem. Two axes were in play: **how to group code** (by technical layer vs. by feature), and **whether to add a blanket `services/` layer and `api/v1/` versioning** up front.

## Options

| | Layered (`routers/` `services/` `models/`) | Feature-modular (`auth/` `problems/` …) |
|---|---|---|
| Cohesion axis | technical layer | feature / domain |
| Understand one feature | open 3–5 sibling dirs | open one folder |
| Blast radius of a change | spread across layers | matches the feature folder |
| Scales as features grow | each layer dir bloats | each module stays small |
| Separation of concerns | enforced by structure | by discipline (+ per-feature `service.py`) |
| Premature abstraction risk | high (empty pass-through services) | low (add a layer when earned) |

## Decision

**Organize `app/` feature-modular** — one module per capability (`auth/`, `problems/`, `content/`, `submissions/`), each co-locating its `router` / `models` / `schemas` (+ `service` only where it has logic). Shared infrastructure lives in `core/`. This is also FastAPI community practice (Netflix Dispatch, fastapi-best-practices).

The load-bearing reason: a change's blast radius should match a directory boundary. Feature modules give that — editing "problems" touches `problems/` — and they keep each module small as the app grows, instead of bloating per-layer directories. We **deliberately rejected** a blanket `services/` layer and `api/v1/` versioning as premature: both add infrastructure for a problem we don't have yet, and both have a clear trigger that would flip the decision later.

**On `services/`** — a layered structure's real wins (structure-enforced separation, reuse across entry points, isolated logic testing) don't apply yet: the routers are thin, there's no shared business logic to hoist, and there's a single entry point (the HTTP API) to reuse *to*. A blanket service layer here would be mostly empty pass-through functions. We add a per-feature `service.py` when a feature earns it — `auth` already has real logic (password hashing, JWTs), so `auth/service.py` exists. The trigger to extract more: a second entry point (worker, CLI) needing to share a feature's logic.

**On `api/v1/`** — versioning protects existing clients from breaking changes. We have exactly one consumer (our own frontend, shipped in lockstep with the backend), so there is no pinned contract to protect and no compatibility benefit to collect — only longer route paths. The trigger to add it: a second, independently-deployed consumer (public API, mobile app, third party).

## Consequences

- A feature's parts live together; navigating and changing one capability touches one folder.
- New features get their own module; shared infrastructure goes in `core/`, never a top-level technical-layer dir.
- Separation of concerns is upheld by discipline plus per-feature services, not by a structural layer — a thin router that grows fat logic is a smell to watch for and extract.
- `service.py` is added per feature on demand (auth has one; problems/content do not). The rule is "add the layer when the feature earns it," which requires judgment on each new feature rather than a blanket convention.
- Model ownership follows the owning domain: `auth` owns `User`; other features import it from `auth.models`.
- Revisiting is cheap and trigger-driven: `services/` extraction when logic is shared across entry points; `api/v1/` when a second consumer appears. Neither requires a rewrite — both are additive when the need is real.
