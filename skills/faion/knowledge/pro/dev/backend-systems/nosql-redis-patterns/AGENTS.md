---
slug: nosql-redis-patterns
tier: pro
group: dev
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Pick the right Redis structure per access pattern: strings for caching, hashes for object fields, lists/streams for queues, sorted sets for sliding-window rate limits, with TTLs on every key.
content_id: "700b75279bdae225"
complexity: medium
produces: spec
est_tokens: 4400
tags: [redis, nosql, caching, rate-limiting, pub-sub]
---
# Redis Data Structure Patterns

## Summary

**One-sentence:** Pick the right Redis structure per access pattern: strings for caching, hashes for object fields, lists/streams for queues, sorted sets for sliding-window rate limits, with TTLs on every key.

**One-paragraph:** Choose the right Redis data structure for each use case: strings for simple caching, hashes for object fields, lists for queues and stacks, sets for unique membership, sorted sets for leaderboards and sliding-window rate limiting, pub/sub for real-time fan-out, and streams for durable event sourcing with consumer groups. Every key gets an explicit TTL or sweep policy. Output is a key-schema YAML naming key pattern + type + TTL + access ops.

**Ефективно для:**

- Designing a key schema for caching and ephemeral state.
- Replacing fixed-window rate limiters with sliding-window sorted sets.
- Choosing Streams over pub/sub when consumer offline → catch-up matters.
- Capping Redis memory growth by enforcing TTLs on every key namespace.

## Applies If (ALL must hold)

- Workload uses Redis (Community, Enterprise, Cluster, or Sentinel).
- Access patterns are known at design time.
- Team can enforce TTLs / sweeps per key namespace.
- Latency-sensitive primary access path (sub-ms reads).

## Skip If (ANY kills it)

- Redis is being used as a primary persistent store of record — antipattern; pick a real DB.
- Workload requires full-text search — use Elasticsearch / Meilisearch.
- Working set exceeds RAM by >10× — paging to disk via on-disk store wins.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Access-pattern list | yaml / md | team |
| Memory budget | yaml | infra |
| Eviction policy | config | ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | This methodology has no upstream dependencies. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | Antipatterns (symptom / root-cause / fix) | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-data-type` | sonnet | Type selection needs judgement on cardinality + atomicity. |
| `draft-schema` | sonnet | Schema authoring benefits from sonnet. |
| `validate-output` | haiku | Schema check is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/key-schema.yaml` | Redis key schema skeleton |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-nosql-redis-patterns.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/dev/backend-systems/`
- [[nosql-mongodb-patterns]]
- [[nosql-cassandra-patterns]]
- [[nosql-neo4j-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
