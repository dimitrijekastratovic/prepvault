# ADR-0002: Adopt uv for Python dependency management

**Status:** Accepted
**Date:** 2026-05-26

## Context

PrepVault's Python dependencies were managed via a single `requirements.txt` produced by `pip freeze`. Every package — direct and transitive — was pinned to an exact version. While this gave reproducibility, it produced a structural problem that surfaced in two consecutive Dependabot failures:

- **PR #50** (`Bump the python-minor-and-patch group`): bumped `pydantic-core` to 2.47.0 while `pydantic` resolved to 2.13.4, which pins `pydantic-core==2.46.4` as a peer dependency. Pip could not resolve the graph and the install failed.
- The same class of failure would reappear on any future Dependabot run that bumped two tightly-coupled packages independently (`httpcore`/`h11`, `starlette`/`fastapi`, etc.).

The root cause: `requirements.txt` treated transitive dependencies as if they were direct, and Dependabot updates each pinned line independently without solving the full dependency graph. Of 27 lines in `requirements.txt`, only ~8 corresponded to packages actually imported by application code; the rest were transitive and should not have been managed by Dependabot at all.

Compounding factors:
- No separation between runtime and dev dependencies — production containers shipped `pytest` and `ruff`.
- No standard project metadata file (`pyproject.toml`) despite this being the modern Python convention (PEP 621).
- Lockfile and "what we actually depend on" were the same file, making the human-readable surface noisy.

## Options considered

### Option 1: Strip transitive pins from `requirements.txt`
Keep only direct dependencies; let pip resolve transitives at install time.
- ✅ Minimal change
- ❌ Loses reproducibility — installs two weeks apart could pull different transitive versions
- ❌ No separation of runtime vs dev
- ❌ Doesn't address the underlying tooling gap

### Option 2: Adopt `pip-tools` (`requirements.in` → `requirements.txt`)
Direct deps in `.in` files; `pip-compile` generates pinned `.txt` lockfiles.
- ✅ Mature, battle-tested, ~10 years old
- ✅ Solves the conflict class (whole-graph resolution)
- ✅ Native Dependabot support
- ❌ Still uses the older `requirements*` file format rather than `pyproject.toml`
- ❌ Slower than modern alternatives
- ❌ Requires separate tools for virtualenv management (`virtualenv` / `venv`)

### Option 3: Adopt `uv`
A single Rust-based tool (by Astral, makers of `ruff`) that handles dependency resolution, lockfile generation, virtualenv management, and command execution. Uses `pyproject.toml` (PEP 621) for project metadata and `uv.lock` for the lockfile.
- ✅ Whole-graph resolution — structurally prevents the PR #50 class of failure
- ✅ `pyproject.toml` is the actual Python packaging standard
- ✅ 10–100× faster than pip-tools for install and resolve
- ✅ First-class dev-dependency support (`[dependency-groups]`)
- ✅ Cross-platform lockfile — one `uv.lock` works on macOS dev and Linux prod
- ✅ Native Dependabot support (as of 2025)
- ✅ Replaces several tools at once (`pip`, `pip-tools`, `virtualenv`, optionally `pyenv`)
- ❌ Newer tool (initial release 2024) — less long-tail community knowledge than pip
- ❌ Single-vendor (Astral); ecosystem risk if direction changes

## Decision

**Adopt `uv` as the sole Python dependency management tool for PrepVault.**

Concretely:
- Direct dependencies are declared in `pyproject.toml` (runtime under `[project.dependencies]`, dev under `[dependency-groups.dev]`).
- The fully resolved dependency graph is locked in `uv.lock`, which is committed.
- `requirements.txt` is deleted.
- The Dockerfile installs production dependencies via `uv sync --frozen --no-dev`.
- CI installs all dependencies (including dev) via `uv sync --frozen` using the `astral-sh/setup-uv` action.
- Dependabot is configured against the `uv` ecosystem so it updates `uv.lock` atomically rather than bumping individual lines.

## Consequences

**Positive:**
- The PR #50 class of failure (mismatched peer-pinned packages) becomes structurally impossible — `uv.lock` is generated atomically from the full graph.
- Production containers no longer ship `pytest` or `ruff`, reducing image size and attack surface.
- `pyproject.toml` becomes the single source of project metadata, aligning with PEP 621 and improving readability.
- Significantly faster CI: `uv sync` installs in seconds rather than tens of seconds.
- Establishes a clear contributor workflow: `uv add <pkg>`, `uv run <cmd>`, `uv sync`.
- Cross-platform lockfile means macOS dev environments and Linux production resolve to the same versions.

**Negative / accepted trade-offs:**
- Contributors must install `uv` (one binary; `brew install uv` on macOS, install script on Linux). Documented in `CONTRIBUTING.md`.
- The repo now depends on a single-vendor tool (Astral). Mitigation: `uv.lock` and `pyproject.toml` are both portable formats — migration off uv would be mechanical, not a rewrite.
- `uv` is younger than pip and pip-tools; some edge-case bug reports may be sparse. The core resolver is mature enough for production use as of 2026.
- Existing CONTRIBUTING / README references to `pip install` must be updated.
