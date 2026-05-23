# Cache Write Patterns (Cache-Aside, Write-Through, Write-Behind)

## Summary

**One-sentence:** Produces a per-entity write-side cache spec: cache-aside (lazy), write-through (sync DB+cache), write-behind (async DB flush); selection by consistency budget + write frequency.

**Ефективно для:**

- Read-heavy entities with bounded write rate.
- Mixed-workload entities where read latency matters more than write cost.
- High-throughput write workloads tolerant of eventual consistency.
- Cache-first architectures (Redis as authority during outages).

**One-paragraph:** Three patterns govern how data enters and exits the cache relative to the database. Cache-aside (lazy load) is the default: check cache, miss, load DB, populate. Write-through keeps cache and DB in sync on every write at the cost of write latency. Write-behind accepts eventual DB consistency in exchange for high write throughput. Pick one per entity type based on consistency budget and write frequency.

## Applies If (ALL must hold)

- Entity has both reads and writes against the cache layer.
- Consistency budget per entity is documented.
- Write rate and read rate are measured.
- Failure mode on write failure is decided (DB-first vs cache-first).

## Skip If (ANY kills it)

- Read-only entities — only read patterns apply.
- No DB behind the cache (cache is the source of truth).
- Per-request entities — caching gives no win.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Per-entity read / write rate | telemetry | SRE |
| Consistency SLO per entity | product decision | PM |
| Failure-mode policy (DB-first vs cache-first) | decision doc | tech lead |
| Cache layer (Redis) ACL | infra doc | SRE |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[caching-invalidation]]` | purge semantics |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input / action / output per step | ~900 |
| `content/05-examples.xml` | recommended | one end-to-end worked example | ~600 |
| `content/06-decision-tree.xml` | essential | run / skip router referencing rule ids | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-entity` | haiku | Read-heavy / write-heavy / mixed. |
| `pick-pattern` | sonnet | Maps SLO + rates to pattern. |
| `draft-write-wrapper` | sonnet | Generates the wrapper with retry / outbox. |

## Templates

| File | Purpose |
|------|---------|
| `templates/caching-write-patterns.json` | JSON Schema for the Cache Write Patterns (Cache-Aside, Write-Through, Write-Behind) output contract |
| `templates/caching-write-patterns.md` | Markdown skeleton with the required fields |
| `templates/_smoke-test.md` | Filled-in minimum viable example of a caching-write-patterns record |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-caching-write-patterns.py` | Enforce the Cache Write Patterns (Cache-Aside, Write-Through, Write-Behind) output contract | After subagent returns, before downstream consumer reads |

## Related

- [[caching-invalidation]]
- [[caching-stampede-prevention]]
- [[caching-http-headers]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) does an existing artefact already cover this gap? Routes to run / skip / update. Every conclusion references a rule id from `content/01-core-rules.xml`.
