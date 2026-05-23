# Rate Limiting

## Summary

**One-sentence:** Rate-limiting spec: algorithm (token bucket / fixed window / sliding log), key strategy (user / IP / tenant), storage (Redis), 429 response shape with Retry-After, and bypass list for health checks.

**One-paragraph:** Rate limiting fails when the algorithm is picked by intuition (per-minute counters reset cliffs), when the key is wrong (per-IP behind a NAT throttles a whole office), when the storage is unbounded (Redis OOMs on the limit keys themselves), and when the 429 response lacks Retry-After so clients hammer back instantly. This methodology produces a spec naming algorithm, key, storage backend with TTL, the 429 contract (status + Retry-After + RateLimit-Remaining headers), and a bypass list (health, metrics).

**Ефективно для:**

- API під DDoS / scraping - запровадити перші ліміти.
- Per-tenant ізоляція - один tenant не повинен валити інших.
- Login endpoint - захист від brute force.
- External API quota - дотримуватись upstream обмежень.
- Fair-use на free тарифі - cap на безкоштовних користувачів.

## Applies If (ALL must hold)

- Service exposes an HTTP API with public or multi-tenant traffic.
- Risk of abuse (scraping, brute force, runaway client) is non-zero.
- Redis or compatible in-memory store is available.
- Owner can sign off limit numbers per endpoint class.

## Skip If (ANY kills it)

- Service is internal-only behind authenticated VPN with trusted callers.
- Throughput SLO does not include fair-use constraints.
- Throttling at a sidecar (Envoy, nginx) covers the policy entirely.
- Project is a throwaway prototype with no production users.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Endpoint classification | table of endpoints with class (auth/read/write) | engineering |
| Limit budget | rps per class signed off by owner | product |
| Redis instance | host + ACL + maxmemory policy | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[nosql-patterns]] | Redis key namespace + TTL conventions reused for limit keys. |
| [[api-error-handling]] | 429 response shape inherits Problem+JSON pattern. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules: algorithm per class, key strategy, TTL on limit keys, 429+Retry-After, bypass list, fail-mode, burst documented | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step spec: classify, pick algorithm, pick key, wire storage, define 429 | ~900 |
| `content/05-examples.xml` | essential | Worked example for SaaS multi-tenant API | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-endpoints` | sonnet | Per-endpoint judgement on burst tolerance. |
| `pick-algorithm` | sonnet | Algorithm vs burst tradeoff per class. |
| `draft-redis-keys` | haiku | Mechanical naming + TTL. |
| `audit-bypass-list` | opus | Stakes high; bypassing too much defeats throttle, too little self-DoSes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rate-limits.yaml` | Rate-limit policy YAML with per-class limits and bypass. |
| `templates/middleware.py` | Reference middleware sketch: token-bucket via Redis INCR + TTL. |
| `templates/sliding-window.py` | Redis ZSET-backed sliding window rate limiter with atomic Lua check-and-add. |
| `templates/k6-rl-probe.js` | k6 load-test probe verifying RateLimit-* headers and 429 + Retry-After. |
| `templates/_smoke-test.json` | Minimum viable rate-limit artefact for validator smoke-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rate-limiting.py` | Validate the artefact against `content/02-output-contract.xml` schema. | After draft, before merge; pre-commit. |

## Related

- [[nosql-patterns]]
- [[api-error-handling]]
- [[security-testing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs - traffic shape, key candidate, storage available, monitoring paths - onto a rule from `content/01-core-rules.xml`. Use it before wiring limits: it catches fixed-window cliff, per-IP NAT block, and missing health bypass upstream.
