---
slug: api-monitoring
tier: solo
group: dev
domain: api-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Instrument every production API endpoint with Prometheus metrics (RED method: Rate, Errors, Duration), structured JSON logging with a `request_id` correlator, and separate liveness/readiness health probes.
content_id: "dbf52e174cb37873"
tags: [monitoring, prometheus, slo, structured-logging, health-probes]
---
# API Monitoring

## Summary

**One-sentence:** Instrument every production API endpoint with Prometheus metrics (RED method: Rate, Errors, Duration), structured JSON logging with a `request_id` correlator, and separate liveness/readiness health probes.

**One-paragraph:** Instrument every production API endpoint with Prometheus metrics (RED method: Rate, Errors, Duration), structured JSON logging with a `request_id` correlator, and separate liveness/readiness health probes. Define SLOs before adding metrics — the metrics exist to measure SLO compliance, not the other way around.

## Applies If (ALL must hold)

- Any HTTP/gRPC/GraphQL service running in production with paying users or SLOs.
- You need quantitative answers to "is the API healthy", "is it getting slower", "who broke it".
- Adding a new endpoint or service — instrument before launch, not after the first incident.
- Setting up readiness probes for k8s / systemd / load balancer drain.
- Diagnosing a regression (p95 spiked, error rate climbing) — metrics + logs + traces correlated by request_id.

## Skip If (ANY kills it)

- Throwaway prototype on localhost — Prometheus scrape config is not a learning goal.
- Internal cron job with one user — exit code + email is enough.
- When you do not yet know what "good" looks like (no SLO defined). Pick SLOs first, then instrument.

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

- parent skill: `solo/dev/api-developer/`
