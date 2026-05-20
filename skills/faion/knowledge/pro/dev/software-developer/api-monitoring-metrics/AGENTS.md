---
slug: api-monitoring-metrics
tier: pro
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Instrument every API using the RED method (Rate, Errors, Duration) per endpoint and USE method (Utilization, Saturation, Errors) per resource.
content_id: "0e9c0b186218044b"
tags: [api-monitoring, prometheus, metrics, red-method, observability]
---
# API Metrics Collection: RED/USE with Prometheus

## Summary

**One-sentence:** Instrument every API using the RED method (Rate, Errors, Duration) per endpoint and USE method (Utilization, Saturation, Errors) per resource.

**One-paragraph:** Instrument every API using the RED method (Rate, Errors, Duration) per endpoint and USE method (Utilization, Saturation, Errors) per resource. Expose a /metrics endpoint via Prometheus client. Labels MUST be bounded: method, route template, status class only — never user_id, request_id, IP, or raw path.

## Applies If (ALL must hold)

- Any API that needs production observability before or after launch.
- Adding RED/USE dashboards before a planned launch or scale event.
- Onboarding a new microservice into an existing Prometheus + Grafana stack.
- Migrating from legacy APM SDKs to OpenTelemetry as the standard instrumentation layer.

## Skip If (ANY kills it)

- Pre-product-fit prototypes — /health + log-to-stdout covers the minimal monitoring need without Prometheus setup overhead.
- Internal tools used by fewer than 10 people daily — alert fatigue exceeds incident value.
- Strict-latency embedded or industrial systems where Prometheus client allocations and OpenTelemetry SDK CPU usage break the SLO. Use sampled, async exporters or skip in-process collection.

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

- parent skill: `pro/dev/software-developer/`
