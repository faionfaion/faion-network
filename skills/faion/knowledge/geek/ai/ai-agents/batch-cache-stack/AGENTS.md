---
slug: batch-cache-stack
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: For any non-real-time agent workload (overnight pipelines, eval harnesses, content backfills, dataset labeling), submit requests through the provider's Message Batches / Batch Mode API and put cache_control on the longest stable prefix (system + tools).
content_id: "dcaee0dbf731e5eb"
tags: [batch-api, prompt-caching, cost-optimization, async-pipelines]
---
# Batch API + Prompt Caching Stack

## Summary

**One-sentence:** For any non-real-time agent workload (overnight pipelines, eval harnesses, content backfills, dataset labeling), submit requests through the provider's Message Batches / Batch Mode API and put cache_control on the longest stable prefix (system + tools).

**One-paragraph:** For any non-real-time agent workload (overnight pipelines, eval harnesses, content backfills, dataset labeling), submit requests through the provider's Message Batches / Batch Mode API and put cache_control on the longest stable prefix (system + tools). The 50% batch discount stacks multiplicatively with the 90% prompt-cache-read discount on every batch item that hits the cache, yielding an effective ~5% of synchronous-uncached cost on the cached portion. This requires picking the batch route over real-time AND keeping every batch item's prefix byte-identical so cache lookups succeed.

## Applies If (ALL must hold)

- Async content pipelines tolerating up to 24h latency (neromedia/pashtelka/longlife nightly summarization).
- Eval suites and regression runs over 100s-100ks of fixtures sharing one rubric.
- Bulk extraction / classification / labeling over a static document corpus.
- Large agent backfill jobs (re-tag the last 30 days of news with a new schema).
- Any pipeline where the system prompt + tool definitions are byte-identical across all items.

## Skip If (ANY kills it)

- Interactive chat or any user-facing surface — 24h SLA is unacceptable.
- Real-time tool-use loops where you need streaming and per-call decisions.
- Workloads with strict <1h SLAs — batches can take up to 24h.
- Pipelines whose prefix mutates per item (different system prompt per row) — cache never hits, you pay the 1.25× cache-write tax for nothing.
- OpenAI workloads where you assumed batch+cache stack — they do not on OpenAI; read the provider's pricing carefully.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/ai/ai-agents/`
