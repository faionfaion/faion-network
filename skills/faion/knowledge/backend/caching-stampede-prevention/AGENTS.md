# Cache Stampede Prevention (Distributed Lock, Probabilistic Refresh, Coalescing)

## Summary

**One-sentence:** Produces a stampede-safe cache spec for hot keys: Redis SETNX distributed lock, probabilistic early refresh (XFetch), and request coalescing wrapper; with budgets per pattern.

**Ефективно для:**

- Hot keys with rebuild cost > 100ms.
- Public endpoints with predictable load spikes (launch, push notification).
- Origin databases with limited connection budget.
- Multi-region deployments where stampedes amplify across edges.

**One-paragraph:** A cache stampede (thundering herd) occurs when a popular key expires and many concurrent requests reload it from origin at once. Without a guard, all requests hit the database simultaneously, causing a load spike that can cascade into a full outage. Three patterns prevent this: distributed lock (one process rebuilds, others wait for the new value), probabilistic early refresh (rebuild before expiry with increasing probability — XFetch algorithm), and request coalescing (in-flight dedup so concurrent same-key requests share one origin call).

## Applies If (ALL must hold)

- Key qualifies as 'hot' (top-10 by request rate or rebuild cost).
- Origin rebuild is non-trivial (DB query, LLM call, computation).
- Cache layer supports atomic SETNX (Redis / Memcached).
- Tail-latency budget tolerates a small wait for the rebuild leader.

## Skip If (ANY kills it)

- Cold or rarely-accessed keys — stampede risk is negligible.
- Rebuild cost ≪ network roundtrip — lock overhead is worse than the stampede.
- Write-through cache populated by writers, not readers.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Hot-key list with rebuild cost + rate | telemetry | SRE |
| Redis cluster ACL for SETNX + EXPIRE | infra doc | SRE |
| Per-key TTL + jitter budget | config | team |
| Origin connection budget | DB ops | SRE |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[backend-systems]]` | host stack |
| `[[caching-invalidation]]` | invalidation patterns |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input / action / output per step | ~900 |
| `content/05-examples.xml` | recommended | one end-to-end worked example | ~600 |
| `content/06-decision-tree.xml` | essential | run / skip router referencing rule ids | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `identify-hot-keys` | haiku | Telemetry threshold filter. |
| `pick-pattern-per-key` | sonnet | Lock vs XFetch vs coalesce decision. |
| `draft-rebuild-wrapper` | sonnet | Generates the safe wrapper code. |

## Templates

| File | Purpose |
|------|---------|
| `templates/caching-stampede-prevention.json` | JSON Schema for the Cache Stampede Prevention (Distributed Lock, Probabilistic Refresh, Coalescing) output contract |
| `templates/caching-stampede-prevention.md` | Markdown skeleton with the required fields |
| `templates/_smoke-test.md` | Filled-in minimum viable example of a caching-stampede-prevention record |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-caching-stampede-prevention.py` | Enforce the Cache Stampede Prevention (Distributed Lock, Probabilistic Refresh, Coalescing) output contract | After subagent returns, before downstream consumer reads |

## Related

- [[caching-invalidation]]
- [[caching-write-patterns]]
- [[caching-in-memory]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) does an existing artefact already cover this gap? Routes to run / skip / update. Every conclusion references a rule id from `content/01-core-rules.xml`.
