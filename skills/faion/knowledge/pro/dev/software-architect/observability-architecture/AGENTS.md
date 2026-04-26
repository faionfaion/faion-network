# Observability Architecture

## Summary

Designing the three-pillar observability stack (metrics, logs, traces) so engineers can answer "why is this broken?" not just "is it broken?". Covers SLI/SLO/error-budget instrumentation, OpenTelemetry collector pipelines, sampling strategies, alerting on burn rate, and cost-optimisation through tiered retention and tail sampling.

## Why

Monitoring tells you when something fails; observability tells you why. Without correlated metrics + logs + traces you cannot answer "why does p99 latency spike for users in EU on Friday afternoons?" Semantic tagging (trace_id on every log line) enables root-cause analysis without pre-configuring every dashboard upfront — critical for unknown failure modes.

## When To Use

- Instrumenting a new service before production launch
- Migrating from ad-hoc logging to structured, correlated telemetry
- Implementing SLO-based alerting (multi-burn-rate alerts)
- Reducing observability costs by replacing head sampling with tail sampling
- Designing OpenTelemetry Collector pipelines for Kubernetes workloads

## When NOT To Use

- A single-process script or cron job — stdout logging is sufficient
- When the existing stack already covers the failure surface and cost is a constraint
- Before SLOs are defined — observability investment without SLOs produces dashboards nobody acts on

## Content

| File | What's inside |
|------|---------------|
| `content/01-pillars-and-slo.xml` | Three pillars comparison, RED/USE/Golden Signals methods, SLI calculation, error budget table, error budget policy triggers |
| `content/02-instrumentation.xml` | OpenTelemetry SDK setup, structured logging format, trace context propagation, sampling strategy (head vs tail), LGTM stack overview |
| `content/03-alerting-and-cost.xml` | Multi-burn-rate alert design, runbook template, alert severity routing, data retention tiers, cardinality limits, tail sampling config |

## Templates

| File | Purpose |
|------|---------|
| `templates/otel-collector.yaml` | Production OTel Collector config with tail sampling, batch, memory limiter, and LGTM exporters |
| `templates/prometheus-rules.yaml` | Multi-burn-rate SLO alerting rules + infrastructure/K8s recording rules |
| `templates/instrumentation.py` | FastAPI + OpenTelemetry SDK setup with trace context injection into structured logs |
