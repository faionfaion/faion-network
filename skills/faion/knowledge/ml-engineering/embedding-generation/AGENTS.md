# Embedding Generation

## Summary

**One-sentence:** Produces the embedding-producer config + code (model id, dimension, normalization, batch size, cache layer, retry policy) for a semantic-search / RAG / clustering pipeline.

**One-paragraph:** Embeddings are dense vector representations of text that power semantic search, RAG, clustering, classification, recommendations, and anomaly detection. This methodology covers the producer side only: choose a model whose quality, latency, dimension, and pricing match the workload (delegated to embeddings-model-selection); set up async batching for throughput; cache by content hash to deduplicate; normalize vectors so cosine similarity is dot product; persist to the vector store via a stable schema. The output is a producer config (JSON) + a Python module that emits embeddings deterministically given the same inputs.

**Ефективно для:**

- Будь-якого RAG-пайплайну, де треба перетворити тексти на вектори перед index/upsert.
- Семантичного пошуку поверх документів, тікетів, повідомлень — коли BM25 не вистачає для синонімів / парафразу.
- Кластеризації або topic-modeling: embeddings + HDBSCAN дешевше і часто кращі за LDA.
- Recommender-систем на content-based фільтрі (товари, статті).
- Anomaly-detection у текстових логах (виявлення outliers по cosine-відстані до centroid).

## Applies If (ALL must hold)

- A downstream system (vector DB, KNN index, classifier) needs vector input.
- Source text is available and can be deterministically partitioned (chunked) or used whole.
- A target vector store is chosen OR will be chosen in this iteration (Qdrant, pgvector, Pinecone, Weaviate, Chroma).

## Skip If (ANY kills it)

- Use case is structured/tabular search where BM25 + filters already match user intent — embeddings add cost without recall gain.
- Pipeline is one-off enrichment on &lt;100 documents — running embeddings via a hosted API once is cheaper than building a producer.
- Privacy / sovereignty rules forbid sending text to a hosted embedding API AND no local embedding model is approved — defer to security review first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Source text corpus | strings / files | Product data layer |
| Chunking spec (size, overlap) | YAML | `chunking-strategies` methodology output |
| Selected embedding model | model id + dim | `embeddings-model-selection` output |
| Target vector store handle | client / URL | Infra |
| API key for hosted provider (if applicable) | env var | Secrets manager |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[embeddings-model-selection]] | Decides which model+dimension the producer must use. |
| [[chunking-strategies]] | Decides the input shape (size, overlap) passed to the producer. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: deterministic producer, content-hash cache, async batching, L2-normalize, dimension-locked schema, exponential-backoff retry | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the producer-config artefact: model_id, dim, normalize, batch_size, cache_backend, retry policy | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: dimension drift, non-deterministic chunking, unnormalized cosine, cache by raw text instead of hash | 700 |
| `content/04-procedure.xml` | reference | 5-step build: scope → cache → batch → normalize → persist | 600 |
| `content/06-decision-tree.xml` | essential | Cache + batch + normalization decision tree | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `parse_chunking_spec` | haiku-4-5 | Deterministic parsing. |
| `generate_producer_code` | sonnet-4-6 | Standard code generation. |
| `audit_existing_producer` | sonnet-4-6 | Code review against rules. |

## Templates

| File | Purpose |
|------|---------|
| `templates/producer.py` | Async batched producer skeleton with content-hash cache + retry. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-embedding-generation.py` | Validate a producer-config JSON against the contract. | Pre-commit; CI gate before deploy. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[embeddings-model-selection]] — chooses the model the producer wraps.
- [[embeddings-provider-apis]] — per-provider SDK quirks.
- [[embeddings-batch-and-cache]] — deep dive on batching + caching primitives.

## Decision tree

See `content/06-decision-tree.xml`. Branches on whether the corpus is large enough (≥1k docs → async batching), whether re-runs are common (yes → content-hash cache; no → no cache), and whether downstream uses cosine (yes → L2 normalize). Leaves emit a producer config shape: `cached-async-batched`, `cached-sync`, `noncached-batched`, or `noncached-sync`, each citing a rule id in `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/producer.py`

```python
from __future__ import annotations

import asyncio
import hashlib
import math
from dataclasses import dataclass
from typing import Iterable, Sequence


@dataclass(frozen=True)
class Config:
    model_id: str
    dimension: int
    normalize: bool
    batch_size: int = 1024
    concurrency: int = 4
    max_attempts: int = 5


def _cache_key(text: str, cfg: Config) -> str:
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return f"{h}:{cfg.model_id}:{cfg.dimension}"


def _l2_normalize(v: list[float]) -> list[float]:
    n = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / n for x in v]


async def _call_provider(batch: Sequence[str], cfg: Config) -> list[list[float]]:
    # Replace with provider SDK call. Stub returns zero-vectors for shape only.
    return [[0.0] * cfg.dimension for _ in batch]


async def _retry(coro_fn, cfg: Config):
    import random
    for attempt in range(cfg.max_attempts):
        try:
            return await coro_fn()
        except Exception:
            if attempt == cfg.max_attempts - 1:
                raise
            wait = min(2 ** attempt + random.uniform(0, 1), 60)
            await asyncio.sleep(wait)


async def embed(chunks: Iterable[str], cfg: Config, cache=None) -> list[list[float]]:
    chunks_list = list(chunks)
    out: list[list[float] | None] = [None] * len(chunks_list)
    missing_idx: list[int] = []
    if cache is not None:
        for i, c in enumerate(chunks_list):
            v = cache.get(_cache_key(c, cfg))
            if v is not None:
                out[i] = v
            else:
                missing_idx.append(i)
    else:
        missing_idx = list(range(len(chunks_list)))

    sem = asyncio.Semaphore(cfg.concurrency)
    batches = [missing_idx[i:i + cfg.batch_size] for i in range(0, len(missing_idx), cfg.batch_size)]

    async def run_batch(idxs: list[int]) -> None:
        texts = [chunks_list[i] for i in idxs]
        async with sem:
            vecs = await _retry(lambda: _call_provider(texts, cfg), cfg)
        for i, v in zip(idxs, vecs):
            if cfg.normalize:
                v = _l2_normalize(v)
            assert len(v) == cfg.dimension, "dimension mismatch"
            out[i] = v
            if cache is not None:
                cache.set(_cache_key(chunks_list[i], cfg), v)

    await asyncio.gather(*(run_batch(b) for b in batches))
    assert all(v is not None for v in out), "missing vectors"
    return out  # type: ignore[return-value]
```
