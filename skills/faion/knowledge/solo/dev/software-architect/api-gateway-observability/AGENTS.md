---
slug: api-gateway-observability
tier: solo
group: dev
domain: software-architect
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: API gateway observability covers three pillars: metrics (request rate, latency percentiles, error rate, circuit breaker state, rate limit hits) exported via Prometheus; structured access logging with correlation ID, consumer identity, and upstream latency; and distributed tracing via OpenTelemetry with W3C trace context propagation.
content_id: "8382b79a0458e92b"
tags: [api-gateway, observability, metrics, tracing, opentelemetry]
---
# API Gateway Observability: Metrics, Logging, Tracing, and Alerting

## Summary

**One-sentence:** API gateway observability covers three pillars: metrics (request rate, latency percentiles, error rate, circuit breaker state, rate limit hits) exported via Prometheus; structured access logging with correlation ID, consumer identity, and upstream latency; and distributed tracing via OpenTelemetry with W3C trace context propagation.

**One-paragraph:** API gateway observability covers three pillars: metrics (request rate, latency percentiles, error rate, circuit breaker state, rate limit hits) exported via Prometheus; structured access logging with correlation ID, consumer identity, and upstream latency; and distributed tracing via OpenTelemetry with W3C trace context propagation. Alert on SLO breaches, not raw thresholds, to reduce false positives.

## Applies If (ALL must hold)

- Setting up initial gateway metrics and Prometheus scrape configuration.
- Configuring structured access logging with correlation IDs and consumer identity.
- Integrating distributed tracing (OpenTelemetry, Jaeger, Zipkin, Tempo).
- Defining SLO-based alerts for error rate, latency, and circuit breaker state.
- Building dashboards for request rate, latency percentiles, and upstream health.
- Correlating traces to logs for incident investigation.

## Skip If (ANY kills it)

- Logging every request body at high RPS — log request metadata only (method, path, status, latency, consumer). Body logging at scale saturates storage and violates GDPR/HIPAA.
- Sampling traces at 100% in high-throughput production — use adaptive or rate-based sampling (10% default, 100% for errors and slow requests).
- Alerting on raw request count thresholds — alert on error rate (%) and latency percentiles, which are meaningful regardless of traffic volume.

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
