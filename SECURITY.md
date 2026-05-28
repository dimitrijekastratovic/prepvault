# Security Policy

## Reporting a vulnerability

If you discover a security vulnerability in PrepVault, please report it privately so it can be addressed before public disclosure.

**Preferred method:** [GitHub Security Advisories](https://github.com/dimitrijekastratovic/prepvault/security/advisories/new) — file a private advisory directly on the repo.

**Alternative:** email `kastratovicdimitrije1@gmail.com` with details. Use the subject prefix `[SECURITY]`.

Please include:
- A clear description of the vulnerability
- Steps to reproduce
- Affected version or commit
- Potential impact

## What to expect

- Acknowledgement within 72 hours
- An initial assessment within 7 days
- Coordination on a disclosure timeline once a fix is in progress

## Scope

PrepVault is currently in active development and **not yet deployed to production**. The security policy will tighten as the project matures into a public service.

For now, in-scope concerns include:
- Authentication or session handling flaws
- SQL injection, XSS, CSRF, SSRF in the application code
- Sandboxing or escape issues in the code execution layer (Judge0)
- Sensitive data exposure in logs, errors, or git history

Out of scope:
- Vulnerabilities in third-party dependencies (please report those to the upstream project, though notes here are welcome)
- Issues requiring physical access to a contributor's machine
- Social engineering of contributors

## Known and accepted trade-offs

### Judge0 worker runs as a privileged container

The `judge0-worker` service in `docker-compose.yml` runs with `privileged: true`. This is required for Judge0's `isolate` sandbox, which depends on Linux cgroups and namespaces to enforce per-submission CPU, memory, and process limits on user-submitted code.

Mitigations in place:
- The worker is on `judge0_internal_net` only — it cannot reach the application database, the application, or anything outside Judge0's internal network at the Docker layer.
- The Judge0 API is the only entry point exposed to the application; the worker is not directly reachable from anywhere else.
- See [ADR-0003](docs/adr/0003-code-execution.md) for the full reasoning on the executor choice and the trade-offs that come with it.

This trade-off will be revisited if/when the project moves to a hosting platform that disallows privileged containers, or if an equivalent rootless sandbox becomes practical.
