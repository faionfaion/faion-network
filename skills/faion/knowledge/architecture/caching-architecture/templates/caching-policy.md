# purpose: Caching policy template.
# consumes: inputs declared in AGENTS.md Prerequisites; schema in content/02-output-contract.xml
# produces: a caching-architecture artefact validating against scripts/validate-caching-architecture.py
# depends-on: content/01-core-rules.xml, content/02-output-contract.xml
# token-budget-impact: ~400-1500 tokens once filled
---
artefact_id: caching-policy-<system>-2026-05-23
owner: <Full Name> <email>
version: 1.0.0
last_reviewed: 2026-05-23
---

## Data classes

| Class | Pattern | TTL | Invalidation | Layer |
|-------|---------|-----|--------------|-------|
| product-detail | cache-aside | 5 min | on write | redis |
| product-list-by-category | read-through | 2 min | on category write | redis |
| customer-cart | write-through | 30 min | on cart update | redis |
| checkout-session | no-cache | n/a | n/a | n/a |
| analytics-rollup | write-behind | 1 hr | hourly batch | redis + db |

## Single-flight policy

Endpoints with cache-aside MUST use single-flight (per-key lock) to prevent thundering herd on cache miss.

## Stampede protection

Cache TTL randomized ±10% jitter to avoid synchronized expiry.

## Monitor

- Hit rate per class (Prometheus).
- p95 latency per class.
