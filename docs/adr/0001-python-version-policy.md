# ADR-0001: Standardize on Python 3.12 and require ADRs for major version bumps

**Status:** Accepted
**Date:** 2026-05-25

## Context

PrepVault's backend (FastAPI) currently runs on Python 3.10 across three environments: local development, CI (`actions/setup-python`), and the production container image (`python:3.10-slim`).

Two pressures forced a decision:

1. **Python 3.10 reaches end-of-life on 2026-10-04.** After that date it receives no security patches, which is incompatible with our production-grade standard.
2. **Dependabot opened a PR bumping the base image from `3.10-slim` to `3.14-slim`.** The build failed because Python 3.14 is too new — `psycopg2-binary` and likely other packages have no pre-built wheels for it yet. This revealed that automated major version bumps for the language runtime are unsafe and need to be a deliberate decision, not a routine dependency update.

The ecosystem reality in May 2026:
- 3.10 — supported until October 2026, then EOL
- 3.11 — supported, mature, wheels universally available
- 3.12 — supported, mature, broad wheel coverage, the current default for most managed runtimes
- 3.13 — supported, growing wheel coverage but some lag in scientific/native packages
- 3.14 — released, ecosystem not yet caught up (confirmed by the failed Dependabot PR)

## Options considered

### Option 1: Stay on 3.10 until forced to upgrade
- ✅ Zero work now
- ❌ EOL in ~5 months; would have to upgrade under deadline pressure
- ❌ Misses performance and typing improvements already shipped in 3.11+
- ❌ Inconsistent with the project's production-grade bar

### Option 2: Upgrade to 3.12
- ✅ Mature, broad wheel coverage, no ecosystem gaps for our stack
- ✅ Significant performance improvements over 3.10 (10–15% on typical workloads)
- ✅ Modern typing features (PEP 695 generics) available
- ✅ One coordinated upgrade rather than two
- ❌ Requires a deliberate upgrade pass across Dockerfile, CI, and any local dev docs

### Option 3: Upgrade to 3.13 (latest stable)
- ✅ Newest stable
- ❌ Some packages in the broader ecosystem still lag on 3.13 wheels
- ❌ Marginal benefit over 3.12 for this project's workload
- ❌ Higher risk of edge-case breakage for negligible gain

### Option 4: Jump straight to 3.14 (what Dependabot proposed)
- ❌ Ecosystem not ready — confirmed by `psycopg2-binary` wheel build failure
- ❌ Likely other packages would surface similar issues
- ❌ Bleeding-edge runtime is not appropriate for a portfolio project demonstrating production discipline

## Decision

**Standardize on Python 3.12 across all environments (local, CI, container).** The upgrade will be performed as a single coordinated change before 3.10 reaches EOL.

**Any future major Python version bump (3.12 → 3.13, 3.13 → 3.14, etc.) requires a new ADR.** Dependabot is configured to suppress major-version PRs for the Python base image so they cannot be merged accidentally.

## Consequences

**Positive:**
- Removes the 2026-10-04 EOL pressure with margin
- Unlocks PEP 695 generics, `typing.override`, and the 3.11/3.12 performance gains
- One upgrade window instead of two (3.10 → 3.12 covers two minor versions at once)
- Establishes the pattern that language-runtime changes are architectural, not dependency-management noise

**Negative / accepted trade-offs:**
- Coordinated upgrade work: Dockerfile, `ci.yml`'s `setup-python`, contributor docs, and local `.python-version` (if added) must all change together
- Any 3.10-only behavior in our code (unlikely but possible) must be audited before the bump
- Local development environments running 3.10 will need to upgrade — currently only one contributor, so low cost

**Follow-up actions tracked elsewhere:**
- Create a Phase-tagged issue: "Upgrade Python 3.10 → 3.12 across Dockerfile, CI, and dev docs"
- Address the separate CI/runtime drift issue: CI currently installs deps on the bare runner instead of inside the container image, meaning CI tests a different Python than production runs. Out of scope for this ADR.
