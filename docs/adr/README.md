# Architecture Decision Records

This directory contains the Architecture Decision Records (ADRs) for PrepVault — short documents capturing significant architectural choices, the context that drove them, and their consequences.

## Why ADRs?

Code shows *what* was built. ADRs show *why*. They prevent re-litigating settled decisions, give future contributors (and future-you) the reasoning behind the architecture, and make trade-offs explicit.

## Format

Each ADR follows a lightweight template:

- **Context** — the problem and constraints
- **Options considered** — with pros and cons
- **Decision** — the chosen option and core reasoning
- **Consequences** — what this unlocks, locks in, or makes harder

ADRs are numbered sequentially (`0001`, `0002`, ...) and named with a kebab-case slug describing the decision (e.g. `0001-code-execution.md`).

## Index

| # | Title | Status |
|---|---|---|
| [0001](0001-python-version-policy.md) | Standardize on Python 3.12 and require ADRs for major version bumps | Accepted |
| [0002](0002-dependency-management-with-uv.md) | Adopt uv for Python dependency management | Accepted |

ADRs are added as decisions are made — see [ROADMAP.md](../../ROADMAP.md) for upcoming phases that will require ADRs.
