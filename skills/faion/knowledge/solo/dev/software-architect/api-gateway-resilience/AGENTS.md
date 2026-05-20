---
slug: api-gateway-resilience
tier: solo
group: dev
domain: software-architect
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Resilience at the gateway layer means applying multi-level rate limiting to prevent abuse, circuit breakers to stop cascading failures, retries with exponential backoff to absorb transient errors, and tiered timeouts matched to backend SLAs.
content_id: "30b3abaca31cd7d1"
tags: [api-gateway, resilience, rate-limiting, circuit-breaker, reliability]
---
# API Gateway Resilience: Rate Limiting, Circuit Breakers, Retries, and Timeouts

## Summary

**One-sentence:** Resilience at the gateway layer means applying multi-level rate limiting to prevent abuse, circuit breakers to stop cascading failures, retries with exponential backoff to absorb transient errors, and tiered timeouts matched to backend SLAs.

**One-paragraph:** Resilience at the gateway layer means applying multi-level rate limiting to prevent abuse, circuit breakers to stop cascading failures, retries with exponential backoff to absorb transient errors, and tiered timeouts matched to backend SLAs. Each mechanism protects the backend from overload and the client from opaque failures.

## Applies If (ALL must hold)

- Configuring multi-level rate limits (global / per-API / per-consumer / per-route).
- Adding circuit breakers for all backend upstreams.
- Designing retry policies with exponential backoff and jitter.
- Setting connection, read, write, and overall request timeouts.
- Planning fallback responses and graceful degradation for backend failures.
- Implementing adaptive rate limiting based on error rates, latency, or backend health.

## Skip If (ANY kills it)

- Circuit breakers on health-check upstreams — wiring breakers on /health polls causes self-inflicted outages. Exclude health endpoints from the circuit.
- Retries on non-idempotent operations (POST, PATCH, DELETE with side effects) — retrying creates duplicate transactions. Only retry GET and safe/idempotent operations unless the backend is explicitly idempotent-safe.
- Rate limiting with local (non-distributed) storage in a multi-node gateway deployment — local mode does not share counters across nodes; force redis or cluster mode.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `solo/dev/software-architect/`
