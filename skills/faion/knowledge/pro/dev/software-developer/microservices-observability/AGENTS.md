---
slug: microservices-observability
tier: pro
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Ship the 3 observability pillars (structured logs, RED/USE metrics, distributed tracing) with W3C trace-context propagation across every microservice.
content_id: "dd9c0eb054b416b2"
complexity: medium
produces: spec
est_tokens: 5200
tags: [microservices, observability, tracing, metrics, logging, otel]
---
# Microservices Observability

## Summary

**One-sentence:** Ship the 3 observability pillars (structured logs, RED/USE metrics, distributed tracing) with W3C trace-context propagation across every microservice.

**One-paragraph:** Microservice observability rests on three pillars: structured logs (JSON with trace_id), RED metrics (rate/errors/duration per endpoint), and distributed tracing via OpenTelemetry with W3C trace-context propagation. Every inbound + outbound call must carry the trace header; every log must include the active trace_id. Skipping one pillar breaks the entire correlation story. The spec output is a service-level observability checklist + the OTel SDK + collector config.

**Ефективно для:**

- Полісервісні архітектури з ≥3 сервісами і необхідністю end-to-end debugging.
- Migration з ad-hoc print-logging до структурованого JSON + trace correlation.
- Wire-up OpenTelemetry (auto + manual instrumentation) для request flow tracing.
- Define SLOs: RED metrics, error budget, alert policies.

## Applies If (ALL must hold)

- Architecture has ≥3 services with inter-service calls.
- Engineering team owns the deployment + can install agents/SDKs.
- Observability backend available (Tempo + Grafana, Datadog APM, Honeycomb, Dynatrace).
- Need SLO measurement against an error budget.

## Skip If (ANY kills it)

- Monolith — single-process tracing is overkill; structured logs + metrics suffice.
- Strict compliance restricts log/trace export (offline-only environments) — see custom-flow methodology.
- Hobby project with <100 req/day — instrumentation cost outweighs benefit.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Service inventory | list + ownership | service catalog |
| Observability backend | OTLP endpoint + access tokens | platform |
| Logging library | structured JSON logger (Logback JsonEncoder / pino / zap) | language ecosystem |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[microservices-inter-service-comm]] | Trace propagation rules depend on call style. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: three-pillars-required, w3c-trace-context, trace-id-in-logs, red-metrics-per-endpoint, no-pii-in-spans | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for spec + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `install-otel-sdk` | sonnet | Templated agent installation per language. |
| `design-slo-and-alerts` | opus | Error budget + alert tuning is high-judgment. |
| `lint-println` | haiku | Mechanical grep for unstructured logging. |

## Templates

| File | Purpose |
|------|---------|
| `templates/observability-spec.md` | Service-level observability spec listing pillar status + SLO + alert rules |
| `templates/otel-config.yaml` | OpenTelemetry Collector config: receivers + processors + exporters |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-microservices-observability.py` | Validate the observability spec artefact against the schema | Pre-commit + CI |

## Related

- [[microservices-circuit-breaker]]
- [[microservices-inter-service-comm]]
- [[api-monitoring-metrics]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, stack, runtime, scale, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
