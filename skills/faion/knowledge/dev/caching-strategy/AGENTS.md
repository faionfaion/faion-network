# Caching Strategy

## Summary

**One-sentence:** Picks one of four canonical cache patterns (cache-aside, write-through, write-behind, read-through), sizes the TTL + key strategy, and emits an invalidation contract with measurable hit-rate target.

**One-paragraph:** Caches solve latency but introduce three new problems: staleness, stampedes, and key collisions. This methodology picks one of four patterns based on read/write ratio and consistency tolerance, sizes per-key TTL with jitter, declares an explicit invalidation contract (publish event / write-through / TTL-only), adds single-flight protection against stampedes, and sets a measurable hit-rate target with an alert below the floor.

**Ефективно для:**

- Solo dev adding Redis in front of a hot endpoint that does 12k QPS.
- Replacing a write-through that turned every write into a P0 outage when Redis blipped.
- Adding single-flight to stop thundering-herd on cache-miss for a popular key.
- Setting an invalidation contract so other services know how to flush on data change.

## Applies If (ALL must hold)

- Hot path has a clear read/write ratio (&gt;5:1 reads).
- Cache store available (Redis / Valkey / Memcached / in-memory).
- Stale-tolerance budget is known (e.g. 30s acceptable, 5min not).
- Author has authority to ship cache + invalidation on the same change.

## Skip If (ANY kills it)

- Pure write workload (cache cost outweighs).
- Hard real-time consistency requirements (e.g. payment authorisation).
- Endpoint with &lt;10 RPS where DB round-trips are fine.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Endpoint + read/write ratio | QPS sample | APM |
| Source-of-truth data store | Postgres / etc. | platform |
| Cache store | Redis / Valkey | platform |
| Stale-tolerance SLA | seconds | PM / architect |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[api-rate-limiting]] | Cache fronts the same endpoints; both share metrics. |
| [[observability-architecture]] | Hit-rate + p95 alerts cross-reference. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + sourced rationale | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes by observable signals to a rule from 01-core-rules.xml | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `caching_strategy_draft` | sonnet | Bounded synthesis. |
| `caching_strategy_validate` | haiku | Mechanical schema check. |
| `caching_strategy_review` | sonnet | Judgement on borderline cases. |

## Templates

| File | Purpose |
|------|---------|
| `templates/cache-aside.py` | Stdlib cache-aside helper with jittered TTL + single-flight |
| `templates/cache-singleflight.py` | Async single-flight skeleton with Redis NX-SET mutex against thundering herd |
| `templates/output-schema.json` | JSON Schema (draft-07) for the caching-strategy artefact |
| `templates/_smoke-test.json` | Minimum viable filled-in caching-strategy artefact for validator round-trip |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-caching-strategy.py` | Validate caching-strategy artefact against schema | Pre-commit; CI on each artefact change |

## Related

- [[api-rate-limiting]]
- [[observability-architecture]]
- [[database-design]]
- [[api-rest-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates on the schema's required cross-field checks; every leaf references a rule in `01-core-rules.xml`.
