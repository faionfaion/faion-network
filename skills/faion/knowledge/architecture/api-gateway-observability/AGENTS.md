# API Gateway Observability

## Summary

**One-sentence:** Three pillars at the gateway edge: Prometheus metrics, structured access logs with correlation ID, and W3C-context OpenTelemetry traces.

**One-paragraph:** Defines the observability config for the gateway layer: request-rate / latency-percentile / error-rate / circuit-breaker-state metrics scraped by Prometheus; access logs with correlation_id + consumer_id + upstream_latency_ms; OpenTelemetry traces with W3C tracecontext propagation. Output is a gateway observability config artefact plus a dashboard/alert pack.

**Ефективно для:**

- паст-готова основа для повторюваної задачі 'API gateway observability' — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф конфігу до того, як він потрапить у CI.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- You run an API gateway (Kong, Tyk, Apollo Router, AWS APIGW, Traefik, Envoy) in production.
- You have or plan a Prometheus + Grafana + tracing stack (Tempo / Jaeger / Honeycomb).
- You need SLO/SLI reporting at the gateway boundary.

## Skip If (ANY kills it)

- Pure pass-through nginx with no app-layer routing — gateway observability adds little.
- No metrics/tracing stack and no plan to add one within the quarter.
- Dev-only environment with no SLO commitments.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Gateway product + version | name + semver | deployment manifest |
| Metrics backend endpoint | URL | platform team |
| Tracing backend endpoint | URL | platform team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-architect/api-gateway-patterns` | Defines the gateway role this config instruments. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the observability config + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~800 |
| `content/04-procedure.xml` | medium | 5-step procedure: pick stack → metrics → logs → traces → SLO dashboard | ~700 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-observability-config` | sonnet | Template fill from gateway + backend selection. |
| `design-slo-dashboard` | sonnet | SLO/SLI panel design. |
| `cross-gateway-trace-audit` | opus | Cross-component propagation correctness. |

## Templates

| File | Purpose |
|------|---------|
| `templates/observability.yaml` | Gateway observability config with metrics, logs, and tracing endpoints. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-api-gateway-observability.py` | Validate the output artefact against the schema in `content/02-output-contract.xml`. | After subagent returns, before downstream consumer reads. |

## Related

- [[api-gateway-patterns]]
- [[api-gateway-resilience]]
- [[api-gateway-security]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/observability.yaml`

```yaml
artefact_id: api-gateway-observability-<client>-2026-05-23
owner: <Full Name> <email>
version: 1.0.0
last_reviewed: 2026-05-23

gateway:
  product: kong
  version: 3.6

metrics:
  prometheus:
    enabled: true
    listen: 0.0.0.0:9090
    histogram_buckets_seconds: [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10]

logging:
  format: json
  fields:
    - timestamp
    - correlation_id
    - consumer_id
    - method
    - path
    - status
    - upstream_latency_ms
    - gateway_latency_ms

tracing:
  otlp:
    endpoint: http://tempo:4317
    propagator: tracecontext
    sample_ratio: 0.1
```
