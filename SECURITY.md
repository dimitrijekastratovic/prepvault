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
- Sandboxing or escape issues in the (planned) code execution layer
- Sensitive data exposure in logs, errors, or git history

Out of scope:
- Vulnerabilities in third-party dependencies (please report those to the upstream project, though notes here are welcome)
- Issues requiring physical access to a contributor's machine
- Social engineering of contributors
