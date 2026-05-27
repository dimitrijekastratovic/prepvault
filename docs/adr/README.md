# Architecture Decision Records

This directory contains the Architecture Decision Records (ADRs) for PrepVault — short documents capturing significant architectural choices, the context that drove them, and their consequences.

## Why ADRs?

Code shows *what* was built. ADRs show *why*. They prevent re-litigating settled decisions, give future contributors (and future-you) the reasoning behind the architecture, and make trade-offs explicit.

## Format

Each ADR is short and decision-focused:

- **Context** — the problem, the constraints, and what triggered the decision *now*
- **Options** — a comparison table, not paragraph-per-option
- **Decision** — the chosen option and the load-bearing reasoning (2–3 sentences)
- **Consequences** — what this unlocks, locks in, or makes harder (bullets)

Target one screen of rendered markdown. ADRs are numbered sequentially (`0001`, `0002`, ...) and named with a kebab-case slug (e.g. `0003-code-execution.md`).

## Index

| # | Title |
|---|---|
| [0001](0001-python-version-policy.md) | Standardize on Python 3.12 and require ADRs for major version bumps |
| [0002](0002-dependency-management-with-uv.md) | Adopt uv for Python dependency management |
| [0003](0003-code-execution.md) | Self-hosted Judge0 for code execution |

ADRs are added as decisions are made — see [ROADMAP.md](../../ROADMAP.md) for upcoming phases that will require ADRs.
