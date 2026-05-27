# ADR-0002: Adopt uv for Python dependency management

**Date:** 2026-05-26

## Context

The project used `pip` + `requirements.txt` with no lockfile. The trigger was a Dependabot grouped-update PR for Python deps — reviewing it surfaced that we had no way to verify the update was safe (no lockfile to diff against), no separation between production and dev dependencies, and slow resolves on every install. Rather than band-aid the existing setup, we treated this as the moment to adopt a proper dep manager.

Requirements for the replacement:
- Locks transitive versions for reproducible installs
- Separates production and dev dep groups
- Fast enough not to dominate CI time
- Uses standard formats (no proprietary lockfile we'd have to migrate off later)

## Options

| | pip + requirements.txt | pip-tools | Poetry | uv |
|---|---|---|---|---|
| Reproducible installs | no | yes | yes | yes |
| Dep groups (dev/prod) | no | yes (manual) | yes | yes |
| Install speed | slow | slow | slow | ~10× faster (Rust) |
| Project config | scattered | scattered | `pyproject.toml` | `pyproject.toml` |
| Cross-platform lock | no | partial | yes | yes |
| Ecosystem maturity | mature | mature | mature | newer (2024+), Astral-backed |

## Decision

**Adopt `uv`** with `pyproject.toml` + `uv.lock`, both committed.

Wins on speed (Rust resolver, ~10× faster than pip-tools/Poetry — real CI/CD impact), uses standard `pyproject.toml` (no proprietary format), produces a portable cross-platform lockfile, and is backed by Astral (also maintain ruff). Maturity is the one weak axis vs. Poetry, but the format is portable enough that migrating off uv would be mechanical, not a rewrite.

## Consequences

- ~35% faster CI and CD (measured: ~38s → ~25s on dep install)
- Contributors must install `uv` (one binary; documented in `CONTRIBUTING.md`)
- macOS dev and Linux prod resolve to the same versions via the cross-platform lockfile
- Single-vendor dependency on Astral — mitigated by `pyproject.toml` + `uv.lock` being portable standards
- Existing `pip install` references in CONTRIBUTING / README replaced
