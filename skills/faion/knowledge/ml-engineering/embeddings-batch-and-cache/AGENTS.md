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

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-embeddings-batch-and-cache.py` | Validate batch+cache config against contract. | Pre-commit; CI gate. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[embedding-generation]] — parent producer methodology.
- [[embeddings-production-ops]] — runs the resulting config in production.

## Decision tree

See `content/06-decision-tree.xml`. Branches on deployment topology (single-host → SQLite, multi-worker → Redis, ephemeral CI → memory), repeat rate (≥10% → cache mandatory, &lt;10% → cache optional), and provider rate budget (concurrency = floor(TPM / tokens_per_batch / 60)). Leaves emit one of: `redis-async-batched`, `sqlite-async-batched`, `memory-batched`, or `no-cache-batched`, citing rule ids in `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/batch-cache.py`

```python
from __future__ import annotations

import asyncio
import hashlib
import random
from typing import Any, Sequence


def _cache_key(text: str, model_id: str, dim: int) -> str:
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return f"{h}:{model_id}:{dim}"


async def _call_provider(batch: Sequence[str], cfg: dict) -> list[list[float]]:
    # Replace with provider SDK; stub returns zero-vectors of the right dim.
    return [[0.0] * cfg["dimension"] for _ in batch]


async def _retry(fn, max_attempts: int):
    for attempt in range(max_attempts):
        try:
            return await fn()
        except Exception:
            if attempt == max_attempts - 1:
                raise
            await asyncio.sleep(min(2 ** attempt + random.uniform(0, 1), 60))


async def embed(inputs: list[str], cfg: dict, cache: Any = None) -> list[list[float]]:
    n = len(inputs)
    out: list[list[float] | None] = [None] * n
    # 1. Dedup by cache key, remember positions
    uniq_keys: dict[str, int] = {}
    uniq_texts: list[str] = []
    positions: dict[str, list[int]] = {}
    for i, t in enumerate(inputs):
        k = _cache_key(t, cfg["model_id"], cfg["dimension"])
        positions.setdefault(k, []).append(i)
        if k not in uniq_keys:
            uniq_keys[k] = len(uniq_texts)
            uniq_texts.append(t)
    # 2. Cache lookup
    need_call: list[tuple[int, str]] = []  # (uniq_idx, text)
    cached: dict[int, list[float]] = {}
    if cache is not None:
        for u_idx, t in enumerate(uniq_texts):
            k = _cache_key(t, cfg["model_id"], cfg["dimension"])
            v = cache.get(k)
            if v is not None:
                cached[u_idx] = v
            else:
                need_call.append((u_idx, t))
    else:
        need_call = [(i, t) for i, t in enumerate(uniq_texts)]
    # 3. Batch parallel call on missing
    batch_size = cfg["batch"]["size"]
    sem = asyncio.Semaphore(cfg["batch"]["concurrency"])
    batches = [need_call[i:i + batch_size] for i in range(0, len(need_call), batch_size)]
    new_vecs: dict[int, list[float]] = {}

    async def run(batch: list[tuple[int, str]]) -> None:
        async with sem:
            vecs = await _retry(lambda: _call_provider([t for _, t in batch], cfg), cfg["retry"]["max_attempts"])
        for (u_idx, t), v in zip(batch, vecs):
            new_vecs[u_idx] = v
            if cache is not None:
                cache.set(_cache_key(t, cfg["model_id"], cfg["dimension"]), v)

    await asyncio.gather(*(run(b) for b in batches))
    # 4. Reassemble in input order
    for k, idxs in positions.items():
        u_idx = uniq_keys[k]
        v = cached.get(u_idx) or new_vecs[u_idx]
        for i in idxs:
            out[i] = v
    assert all(v is not None for v in out)
    return out  # type: ignore[return-value]
```
