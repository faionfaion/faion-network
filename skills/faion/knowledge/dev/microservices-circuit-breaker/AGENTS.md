# Microservices Circuit Breaker

## Summary

**One-sentence:** Wrap unreliable downstream service calls in a circuit breaker (Resilience4j / Polly / Hystrix-equivalent) that opens on configured failure rate and provides a fallback path.

**One-paragraph:** Circuit breaker is a stateful proxy that monitors call success vs failure rate over a sliding window. When the failure rate crosses a threshold, the breaker opens — short-circuiting subsequent calls to a fallback for a cooldown period — then half-opens to probe recovery. Use it on every cross-service network call. Pair with bulkhead (concurrency cap) + timeout + retry (with backoff + jitter) for full resilience. Without a fallback, the breaker just changes which exception type the caller sees.

**Ефективно для:**

- Кросс-сервісні HTTP/gRPC виклики до downstream services з варіативним SLA.
- Сторонні API (платіжний шлюз, geo-IP, email vendor) з відомими degraded modes.
- Service mesh с потребою stateful resilience: breaker + bulkhead + timeout + retry-budget.
- Backoff cascade prevention: щоб один повільний downstream не обвалив весь stack.

## Applies If (ALL must hold)

- Caller makes synchronous network call to another service it does not own.
- Failure of the downstream has a clear fallback path (cached value, default, degraded UX).
- Caller's SLO is tighter than the downstream's worst-case latency.
- Library available (Resilience4j for JVM, Polly for .NET, opossum for Node).

## Skip If (ANY kills it)

- Single-process app with no network IO — no breaker target.
- Async/queue-backed call — durability handles failures; breaker adds no value.
- No defined fallback — breaker just changes the exception; caller must still handle.
- Strongly-consistent transactional flows where fallback would break invariants.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Downstream client | HTTP/gRPC client method | service inventory |
| Failure SLA budget | max failure rate %, slow-call threshold ms | SRE / SLO |
| Fallback definition | cached / default / degraded path | product |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[microservices-inter-service-comm]] | Pick HTTP vs gRPC vs messaging first; breaker rules differ. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: breaker-per-downstream, explicit-thresholds, fallback-required, metrics-and-alert, no-bare-retry-with-breaker | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for code + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `size-breaker-thresholds` | opus | Tuning requires reading historical SLO data + tradeoff analysis. |
| `wire-decorator` | sonnet | Templated composition pattern. |
| `lint-composition-order` | haiku | Mechanical AST/regex audit. |

## Templates

| File | Purpose |
|------|---------|
| `templates/Resilience4jBreakerConfig.java` | Resilience4j CircuitBreakerRegistry + named breaker for one downstream |
| `templates/PaymentService.java` | Decorator composition Retry(Breaker(Call)) with fallback enqueue |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-microservices-circuit-breaker.py` | Validate the breaker config artefact against the schema | Pre-commit + CI |

## Related

- [[microservices-inter-service-comm]]
- [[microservices-observability]]
- [[microservices-saga-pattern]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, stack, runtime, scale, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
