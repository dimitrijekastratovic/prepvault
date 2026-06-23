# ADR-0006: Codify feature-module conventions

**Date:** 2026-06-23

## Context

[ADR-0005](0005-feature-modular-layout.md) chose a feature-modular layout but left the *internal* conventions of a module unwritten — which files a module has, how it handles errors, how it serializes reads, what status codes it declares. Each feature was then built at a different time to a different implicit standard, and they drifted.

An audit during the submissions work (#61) made the drift concrete: `submissions` raises domain exceptions and translates them in the router, declares `status_code=201`, and serializes reads with `model_validate`; the earlier features (`auth`, `problems`) raise `HTTPException` directly in routers, return `200` from endpoints that create resources, and construct read models by hand. The standard lived only in reviewer memory and conversation, so every new module risked inventing its own variant.

The fix has two halves: retrofit the existing code (tracked separately in #84/#85/#86), and — the subject of this ADR — **write the standard down** so it stops drifting.

## Options

| | Leave it implicit | Inline in CONTRIBUTING.md | ADR + CONVENTIONS.md |
|---|---|---|---|
| Records the *decision* + why | no | weakly | yes (ADR, immutable) |
| Living *how-to* detail | — | mixed with contributor flow | yes (CONVENTIONS.md) |
| Survives reviewer turnover | no | partly | yes |
| Conformance tickets can cite it | no | awkward | yes (#84/#85/#86 → CONVENTIONS.md) |
| Re-litigation risk | high | medium | low |

## Decision

**Split into two artifacts.** An ADR (this file) records the *decision to standardize* and the *why* — immutable, matching ADR-0001–0005. A top-level [`CONVENTIONS.md`](../../CONVENTIONS.md) holds the *living what* — module file layout, error handling, read serialization, success status codes, and test layout/naming — and is updated as conventions evolve.

The load-bearing reason for two artifacts: the *decision* (we standardize feature modules, for consistency and defensibility) is settled and should not churn, while the *rules* will gain detail as features appear. An ADR that listed every rule would need editing on every refinement, defeating its immutability; a CONVENTIONS.md alone would lose the "why we bother" that prevents re-litigation. `submissions` is the reference implementation the document describes.

We considered formalizing layered **Clean / hexagonal architecture** (repository interfaces, use-case classes, DTOs at every boundary) and rejected it as premature for one datastore and one consumer — those abstractions would be empty pass-throughs ([ADR-0005](0005-feature-modular-layout.md), [the design-pattern philosophy](../../CONTRIBUTING.md)). We do adopt its one load-bearing principle: the **dependency rule** — domain logic never depends on the web framework. That is why "services raise domain exceptions and never import `fastapi`; routers/handlers translate at the edge" is a rule in `CONVENTIONS.md`, applied at the seam that earns it rather than across speculative layers.

## Consequences

- New modules have one authoritative place to check before adding files, errors, or endpoints — drift is corrected by review against a written rule, not by memory.
- `CONVENTIONS.md` is the standard that conformance tickets bring existing code up to: #84 (read serialization / N+1), #85 (domain exceptions), #86 (success status codes) reference it.
- The document is descriptive of `submissions` today; when a convention genuinely needs to change, the change lands in `CONVENTIONS.md` (and, if the *decision* itself shifts, a superseding ADR) — not silently in code.
- Slight upkeep cost: a new convention now means a doc edit, not just a code change. Accepted — that visibility is the point.
- Linked from `CONTRIBUTING.md` so contributors meet it in the normal flow.
