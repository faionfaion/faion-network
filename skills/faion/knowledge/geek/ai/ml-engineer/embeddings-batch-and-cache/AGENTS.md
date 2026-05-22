---
slug: embeddings-batch-and-cache
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces an embedding-batch-and-cache config (batch size, parallelism, cache backend + TTL + key scheme) cutting embedding API cost up to 90% on repeat workloads via dedup + content-hash cache + async parallel batching.
content_id: "emb-bc-001239abc456789a"
complexity: medium
produces: config
est_tokens: 3200
tags: [embeddings, batch-api, cache, redis, sqlite, throughput, deduplication]
---
# Embedding Batch Processing and Caching

## Summary

**One-sentence:** Produces a batching + caching config (batch size per provider, parallel concurrency, cache backend, TTL, dedup pass) that cuts embedding API cost 80-95% on repeat workloads while preserving result order.

**One-paragraph:** Two complementary optimizations: batching reduces API overhead 10-100× (a 1000-call sequential pipeline → 10 batches of 100); caching eliminates repeated computation (80% cache hit rate → 80% cost savings). Both require careful keying — cache key MUST include model + dim + content hash, batch results MUST be ordered by input index. This methodology emits a config that names batch.size per provider (OpenAI 2048, Voyage 128, Cohere 96), concurrency by rate budget, backend by deployment topology (Redis shared, SQLite single-host, memory ephemeral), and TTL by content volatility.

**Ефективно для:**

- Індексації великих корпусів (тисячі-мільйони документів), де single-call API спалює виставлений рахунок.
- Чат / search додатків з високою повторюваністю user-queries — cache hits відсікають дзвінок повністю.
- Pipeline-ів з rate-limit вузьким місцем (OpenAI tier 1: 1M tokens/min) — paralel batches вирівнюють throughput.
- Дедуплікації input-у: однакові тексти в корпусі (boilerplate footer, repeated paragraphs) рахуються один раз.
- Local development з SQLite-кешем — не треба піднімати Redis для прототипу.

## Applies If (ALL must hold)

- Embedding pipeline processes ≥1000 inputs OR has a measurable repeat rate (≥10% of inputs recur).
- Throughput requirement ≥10 inputs/second OR batch latency &lt; sum-of-singles latency.
- A cache backend is available or approved (Redis, SQLite, or in-memory dict).

## Skip If (ANY kills it)

- Corpus is &lt;100 inputs total — setup overhead exceeds API savings.
- Input stream is provably unique (UUIDs, timestamps, monotonic IDs concatenated) — cache hit rate stays at 0.
- Quality validation requires per-call telemetry — batching obscures per-input latency tail.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Embedding provider + model id | string | `embeddings-model-selection` output |
| Expected input volume + repeat rate | numbers | Product analytics |
| Rate budget (RPM / TPM) | numbers | Provider dashboard |
| Cache backend handle | client / URL | Infra (Redis) or local FS (SQLite) |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[embedding-generation]] | Wraps the producer this config tunes. |
| [[embeddings-provider-apis]] | Provider-specific batch limits feed batch.size. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: batch-by-provider-limit, preserve-input-order, content-hash-cache-key, dedup-before-call, exponential-backoff | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for batch+cache config | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: cache-by-text-only, order-not-preserved, no-dedup-pass, batch-without-rate-budget | 700 |
| `content/04-procedure.xml` | reference | 5-step build procedure | 500 |
| `content/06-decision-tree.xml` | essential | Backend + parallelism decision tree | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `tune_batch_config` | haiku-4-5 | Math: divide rate by per-input cost. |
| `generate_config_artefact` | sonnet-4-6 | Structured output via forced tool. |

## Templates

| File | Purpose |
|------|---------|
| `templates/batch-cache.py` | Async parallel batched embedder with content-hash cache + order preservation. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-embeddings-batch-and-cache.py` | Validate batch+cache config against contract. | Pre-commit; CI gate. |

## Related

- [[embedding-generation]] — parent producer methodology.
- [[embeddings-production-ops]] — runs the resulting config in production.

## Decision tree

See `content/06-decision-tree.xml`. Branches on deployment topology (single-host → SQLite, multi-worker → Redis, ephemeral CI → memory), repeat rate (≥10% → cache mandatory, &lt;10% → cache optional), and provider rate budget (concurrency = floor(TPM / tokens_per_batch / 60)). Leaves emit one of: `redis-async-batched`, `sqlite-async-batched`, `memory-batched`, or `no-cache-batched`, citing rule ids in `01-core-rules.xml`.
