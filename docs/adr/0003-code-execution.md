# ADR-0003: Self-hosted Judge0 for code execution

**Date:** 2026-05-27

## Context

Phase 5.6 wires up code execution for the playground. The next ten tickets (submission model, executor service, submission endpoints, WebSocket verdict push, UI wiring) all depend on *which* executor we use and *how* it is deployed — none of them can be written without this decision locked in. The repo is also a portfolio showcase, so "demonstrates infra competence" is a real evaluation axis alongside cost and reliability.

A custom judge cluster (gVisor + S3 + RabbitMQ) was already deferred in earlier Phase 5 planning in favour of an off-the-shelf executor. This ADR records *which* executor and *how it is deployed*.

## Options

| | Self-hosted Judge0 | Hosted Judge0 | Piston |
|---|---|---|---|
| Cost at scale | infra only | per-request | infra only |
| Rate limits | none | 50/day free, paid beyond | none |
| Sandboxing | isolate (cgroups + namespaces) | same | lighter |
| Ecosystem | mature, broad language support | same | smaller, fewer languages |
| Ops burden | runs as Compose services | none | single container |
| Portfolio value | high | none | moderate |
| Reversibility | abstraction layer makes all three swappable in one class |

## Decision

**Self-hosted Judge0 via Docker Compose**, behind a `CodeExecutionService` abstraction.

Hosted is eliminated by the free-tier rate limit and zero portfolio value. Piston is the closest runner-up but loses on ecosystem maturity and recognisability. The abstraction layer means the decision is reversible at the cost of one class.

## Consequences

- Heavier `docker-compose.yml`; longer first-time setup for contributors
- Judge0's `isolate` sandbox requires a privileged container — must be network-isolated and documented as a known risk
- Some managed PaaS (e.g. AWS App Runner) disallow privileged containers; future hosting choice must account for this. Fly.io and self-managed VMs are fine.
- Local dev and prod run the same Judge0 — no environment drift on the execution path
- ADR will be revisited if operational cost grows beyond what a single developer can sustain
