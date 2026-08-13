# API Gateway Resilience

## Summary

**One-sentence:** Multi-level rate limiting, circuit breakers, exponential-backoff retries with idempotency, and tiered timeouts at the gateway layer.

**One-paragraph:** Defines gateway resilience as four coordinated controls: rate limiting per-consumer + per-route, circuit breakers per upstream with half-open probes, retries with exponential backoff guarded by Idempotency-Key, and tiered timeouts matched to backend SLAs. Output is a gateway resilience config artefact plus a chaos test plan to validate the controls under load.

**Ефективно для:**

- паст-готова основа для повторюваної задачі 'API gateway resilience' — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф конфігу до того, як він потрапить у CI.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Gateway routes traffic to ≥3 upstreams with different SLA contracts.
- You have observed at least one cascading-failure incident OR you want to prevent one before launch.
- Backend SLAs and per-route latency budgets are known.
- You have a load test harness or plan to add one within the quarter.

## Skip If (ANY kills it)

- Single upstream with single SLA — gateway resilience adds complexity without benefit.
- Read-only static traffic with no rate-limit needs.
- Backends already enforce these controls and gateway would just duplicate them.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Per-upstream SLA | p95 latency + availability target | platform team |
| Per-route traffic profile | RPS + percentiles | observability backend |
| Idempotency-Key support audit | list of mutating routes + idempotency capability | service owners |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-architect/api-gateway-patterns` | Defines the gateway role this config layers controls onto. |
| `solo/dev/software-architect/api-gateway-observability` | Provides the metrics that drive circuit-breaker decisions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules + skip-this-methodology fallback | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the resilience config + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~800 |
| `content/04-procedure.xml` | deep | 5-step procedure: profile traffic → rate limits → circuit breakers → retries → timeouts | ~900 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-resilience-config` | sonnet | Template fill from SLAs. |
| `design-chaos-test` | sonnet | Per-control failure injection plan. |
| `cross-upstream-budget-audit` | opus | Verify aggregated retry/rate-limit budgets do not exceed backend capacity. |

## Templates

| File | Purpose |
|------|---------|
| `templates/resilience.yaml` | Gateway resilience config: rate limits, breakers, retries, timeouts. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-api-gateway-resilience.py` | Validate the output artefact against the schema in `content/02-output-contract.xml`. | After subagent returns, before downstream consumer reads. |

## Related

- [[api-gateway-patterns]]
- [[api-gateway-observability]]
- [[api-gateway-security]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/resilience.yaml`

```yaml
artefact_id: api-gateway-resilience-<client>-2026-05-23
owner: <Full Name> <email>
version: 1.0.0
last_reviewed: 2026-05-23

rate_limits:
  - scope: consumer
    requests_per_minute: 600
    burst: 60
  - scope: route
    route: /api/v1/checkout
    requests_per_minute: 1000
    burst: 100

circuit_breakers:
  - upstream: payment-service
    failure_threshold_pct: 50
    minimum_requests: 20
    open_for_seconds: 30
    half_open_probes: 3

retries:
  - method: GET
    max_attempts: 3
    base_backoff_ms: 100
    max_backoff_ms: 1000
  - method: POST
    max_attempts: 2
    base_backoff_ms: 200
    max_backoff_ms: 1000
    require_idempotency_key: true

timeouts:
  default_ms: 5000
  per_upstream:
    payment-service: 8000
    search-service: 2000
```
