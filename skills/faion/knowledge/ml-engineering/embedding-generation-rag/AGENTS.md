# Embedding Generation

## Summary

**One-sentence:** Generates embedding pipeline — same-model index/query, batched calls (OpenAI ≤2048), SHA-256 cache keys, unit normalization, empty/overlong guards, provider-specific tuning.

**One-paragraph:** Wrong embedding generation produces silent recall regressions. This methodology produces an `EmbeddingService` that pins model+version, batches with provider-correct caps, normalizes to unit length for cosine, caches by SHA-256(model+version+text), rejects empty/overlong texts, and applies provider-specific tuning (Cohere input_type, OpenAI dimensions, single-process SentenceTransformer). Output is a code class consumed by the broader embedding-applications pipeline.

**Ефективно для:**

- New RAG project — embed indexing step.
- Replace per-text loop with batched calls (10–50x speedup).
- Add SHA-256 cache to recurring ingest.
- Migrate Ollama loop → SentenceTransformer for local.
- Cohere input_type compliance (5–10% quality boost).

## Applies If (ALL must hold)

- Embedding new corpus OR rewriting existing pipeline.
- Same embedder used for both indexing AND querying.
- Vector DB available.
- Named owner.

## Skip If (ANY kills it)

- Pure keyword search (no embeddings needed).
- &lt;10-token average texts (BM25 outperforms).
- Low-resource language без multilingual model.
- Existing pipeline validated &lt;90 days.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Embedding model name + version | YAML | service repo |
| Provider client | client | platform |
| Tokenizer (for guard checks) | tokenizer | platform |
| Cache backend (optional) | client | platform |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[embedding-models]]` | Provider-specific quirks. |
| `[[embedding-caching]]` | Cache layer. |
| `[[embedding-applications]]` | Parent pipeline. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules + run/skip terminals | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for embedder-config | ~700 |
| `content/03-failure-modes.xml` | essential | 7 antipatterns with detector + repair | ~900 |
| `content/04-procedure.xml` | essential | 5-step: pin model → wire batch → cache → normalize → guards | ~700 |
| `content/06-decision-tree.xml` | essential | Routes provider + corpus to embedder config | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pin-model-version` | haiku | Config write. |
| `tune-provider-params` | sonnet | Per-provider judgment. |
| `audit-output` | haiku | Schema check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/embedding_service.py` | EmbeddingService class with batching + cache + guards. |
| `templates/embedder-config.json` | Config skeleton. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[embedding-models]]
- [[embedding-caching]]
- [[embedding-cost-optimization]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes by provider + corpus class to embedder config. Walk before wiring.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/embedding_service.py`

```python
from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass
from typing import Any, Callable

PROVIDER_CAPS = {"openai": 2048, "cohere": 96, "voyage": 128, "google": 250, "azure": 2048, "local": 1024}


@dataclass
class EmbedderConfig:
    model_name: str
    model_version: str
    provider: str
    batch_size: int = 256
    normalize: bool = True
    cache_hash_algo: str = "sha256"
    max_input_tokens: int = 8191
    input_type_index: str = "n/a"
    input_type_query: str = "n/a"


def _normalize(v: list[float]) -> list[float] | None:
    n = math.sqrt(sum(x * x for x in v))
    if n < 1e-9:
        return None
    return [x / n for x in v]


@dataclass
class EmbeddingService:
    config: EmbedderConfig
    embed_provider: Callable[[list[str], dict[str, Any]], list[list[float]]]
    tokenize: Callable[[str], list[str]]
    cache_get: Callable[[str], list[float] | None] | None = None
    cache_set: Callable[[str, list[float]], None] | None = None

    def __post_init__(self) -> None:
        if self.config.batch_size > PROVIDER_CAPS.get(self.config.provider, 2048):
            raise ValueError("batch_size > provider cap (rule r2)")
        if self.config.cache_hash_algo != "sha256":
            raise ValueError("cache_hash_algo must be sha256 (rule r3)")
        if self.config.provider == "cohere":
            if not self.config.input_type_index or not self.config.input_type_query:
                raise ValueError("Cohere requires input_type_index + input_type_query (rule r6)")

    def _key(self, text: str) -> str:
        h = hashlib.sha256(text.encode("utf-8")).hexdigest()
        return f"{self.config.model_name}:{self.config.model_version}:{h}"

    def _safe(self, text: str) -> bool:
        if not text or not text.strip():
            return False
        if len(self.tokenize(text)) > self.config.max_input_tokens:
            return False
        return True

    def embed_batch(self, texts: list[str], *, is_query: bool = False) -> dict[str, Any]:
        valid: list[tuple[int, str]] = [(i, t) for i, t in enumerate(texts) if self._safe(t)]
        cached: dict[int, list[float]] = {}
        misses: list[tuple[int, str]] = []
        for i, t in valid:
            if self.cache_get is not None:
                v = self.cache_get(self._key(t))
                if v is not None:
                    cached[i] = v
                    continue
            misses.append((i, t))
        cap = PROVIDER_CAPS.get(self.config.provider, 2048)
        new_vectors: dict[int, list[float]] = {}
        for start in range(0, len(misses), min(self.config.batch_size, cap)):
            chunk = misses[start : start + min(self.config.batch_size, cap)]
            kwargs: dict[str, Any] = {}
            if self.config.provider == "cohere":
                kwargs["input_type"] = self.config.input_type_query if is_query else self.config.input_type_index
            vectors = self.embed_provider([t for _, t in chunk], kwargs)
            for (i, t), v in zip(chunk, vectors, strict=True):
                if self.config.normalize:
                    nv = _normalize(v)
                    if nv is None:
                        continue
                    v = nv
                new_vectors[i] = v
                if self.cache_set is not None:
                    self.cache_set(self._key(t), v)
        result: list[list[float] | None] = [None] * len(texts)
        for i, v in cached.items():
            result[i] = v
        for i, v in new_vectors.items():
            result[i] = v
        return {"vectors": result, "cache_hits": len(cached), "embedded": len(new_vectors), "skipped": len(texts) - len(valid)}
```

### `templates/embedder-config.json`

```json
{
  "model_name": "text-embedding-3-large",
  "model_version": "2026-04",
  "provider": "openai",
  "batch_size": 512,
  "normalize": true,
  "cache_hash_algo": "sha256",
  "max_input_tokens": 8191,
  "input_type_index": "n/a",
  "input_type_query": "n/a"
}
```
