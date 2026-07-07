# Changelog

All notable changes to PrepVault are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `ROADMAP.md` documenting phased plan to production.
- `README.md` rewritten with overview, architecture diagram, getting started, engineering principles.
- `LICENSE` (MIT).
- `SECURITY.md`, `CONTRIBUTING.md`, `CODEOWNERS`.
- Issue templates (task, ADR, bug) and PR template under `.github/`.
- Dependabot configuration for weekly dependency updates.
- `.editorconfig` for cross-editor formatting consistency.
- `.env.example` documenting required environment variables.
- Branch protection ruleset on `main` (PR required, CI must pass, squash merges only, linear history).
- Playground React app scaffolded with Vite + Monaco Editor (`ProblemPanel`, `Editor`, `Header` components, theme toggle, problem list/detail views).

### Changed
- CD workflow image name corrected from `nonamerepo` to `prepvault`.
- Python version changed from 3.10 to 3.12 per ADR-0001

---

<!--
Release entries below this line follow the Keep a Changelog format:

## [0.1.0] - YYYY-MM-DD
### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security
-->
