---
slug: observability-architecture
tier: pro
group: dev
domain: architecture
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Designing the three-pillar observability stack (metrics, logs, traces) so engineers can answer "why is this broken?" not just "is it broken?".
content_id: "794083d3c30cd690"
tags: [observability, monitoring, tracing, logging, slo]
---
# Observability Architecture

## Summary

**One-sentence:** Designing the three-pillar observability stack (metrics, logs, traces) so engineers can answer "why is this broken?" not just "is it broken?".

**One-paragraph:** Designing the three-pillar observability stack (metrics, logs, traces) so engineers can answer "why is this broken?" not just "is it broken?". Covers SLI/SLO/error-budget instrumentation, OpenTelemetry collector pipelines, sampling strategies, alerting on burn rate, and cost-optimisation through tiered retention and tail sampling.

## Applies If (ALL must hold)

- Instrumenting a new service before production launch
- Migrating from ad-hoc logging to structured, correlated telemetry
- Implementing SLO-based alerting (multi-burn-rate alerts)
- Reducing observability costs by replacing head sampling with tail sampling
- Designing OpenTelemetry Collector pipelines for Kubernetes workloads

## Skip If (ANY kills it)

- A single-process script or cron job — stdout logging is sufficient
- When the existing stack already covers the failure surface and cost is a constraint
- Before SLOs are defined — observability investment without SLOs produces dashboards nobody acts on

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

- parent skill: `pro/dev/software-architect/`
