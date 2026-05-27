# ADR-0001: Standardize on Python 3.12 and require ADRs for major version bumps

**Date:** 2026-05-25

## Context

The backend runs on Python 3.10 across local dev, CI, and the production container. Two pressures forced a decision:

1. Python 3.10 reaches end-of-life on **2026-10-04** — no security patches after that, incompatible with the project's production-grade bar.
2. A Dependabot PR bumping the base image to `3.14-slim` failed to build (`psycopg2-binary` has no 3.14 wheels). Major language-runtime bumps are not safe as routine dependency updates.

## Options

| | Stay on 3.10 | Upgrade to 3.12 | Upgrade to 3.13 | Jump to 3.14 |
|---|---|---|---|---|
| Work now | none | one coordinated pass | one coordinated pass | one coordinated pass |
| EOL risk | hits in ~5 months | none | none | none |
| Wheel coverage | universal | universal | minor gaps in native/sci packages | confirmed broken (psycopg2-binary) |
| Performance vs 3.10 | baseline | +10–15% | +10–15% | +10–15% |
| Risk | high (deadline pressure later) | low | moderate | high |

## Decision

**Standardize on Python 3.12 across all environments.** One coordinated upgrade pass before 3.10 EOL.

**Any future major Python bump requires a new ADR.** Dependabot is configured to suppress major-version PRs for the Python base image so they cannot be merged accidentally.

## Consequences

- Removes the 2026-10-04 EOL deadline with margin
- Unlocks PEP 695 generics, `typing.override`, and the 3.11/3.12 performance gains
- Establishes that language-runtime changes are architectural, not dependency noise
- Coordinated change required: Dockerfile, CI's `setup-python`, contributor docs, and `.python-version` if added
- Any 3.10-only behavior in our code must be audited before the bump (low risk — codebase is small and modern)
