# Embedding Caching Patterns

## Summary

**One-sentence:** Embedding cache layer — SHA-256 keyed by (model+version+text), TTL aligned with model version, Redis/Valkey backend, cache-hit metric for cost audit.

**One-paragraph:** Re-embedding the same text wastes API budget. This methodology produces an `EmbeddingCache` class: SHA-256 cache keys composed of (model_name + model_version + text), TTL bounded by model-deprecation calendar, Redis/Valkey backend, per-call cache-hit metric. MD5 explicitly rejected (collision risk at billion-doc scale).

**Ефективно для:**

- RAG re-ingestion pipelines where same docs flow repeatedly.
- Multi-tenant systems де different tenants embed same source.
- Cost audit — cache_hit_rate як KPI.
- Cache invalidation aligned з model deprecation.
- Browser/edge usage де latency &lt; API round-trip required.

## Applies If (ALL must hold)

- Corpus re-ingestion expected (updates / nightly refresh / multi-tenant).
- Cache backend available (Redis / Valkey / DynamoDB).
- Per-vector model_version stored.
- Named owner.

## Skip If (ANY kills it)

- One-shot embedding (corpus indexed once, never updated).
- &lt;5% repeated-text rate (cache hit savings &lt; cost).
- No cache backend.
- Latency requirement met without cache.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Cache backend client (Redis / Valkey) | client | platform |
| Embedding model client | client | platform |
| Model name + version pin | YAML | service repo |
| Cache hit metric collector | platform | observability |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[embedding-generation]]` | Underlying embed call. |
| `[[embedding-cost-optimization]]` | Companion cost methodology. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4 rules + run/skip terminals | ~700 |
| `content/02-output-contract.xml` | essential | JSON Schema for cache-config | ~600 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns | ~700 |
| `content/04-procedure.xml` | essential | 5-step: pick backend → key gen → TTL → metric → audit | ~700 |
| `content/06-decision-tree.xml` | essential | Routes corpus class to cache vs no-cache | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `compute-cache-key` | haiku | Mechanical hash. |
| `evict-by-model-deprecation` | sonnet | TTL judgment. |
| `audit-hit-rate` | haiku | Numeric. |

## Templates

| File | Purpose |
|------|---------|
| `templates/embedding_cache.py` | EmbeddingCache class with SHA-256 + TTL. |
| `templates/cache-config.json` | Config skeleton. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-embedding-caching.py` | Validate cache-config | Pre-commit + CI |

## Related

- [[embedding-generation]]
- [[embedding-cost-optimization]]
- [[embedding-models]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes to cache when repeated-text rate &gt;5% AND backend available. Otherwise direct embed.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/embedding_cache.py`

```python
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class CacheConfig:
    backend: str = "valkey"
    hash_algo: str = "sha256"
    key_components: tuple[str, ...] = ("model_name", "model_version", "text")
    ttl_days: int = 90
    emit_hit_metric: bool = True


@dataclass
class EmbeddingCache:
    config: CacheConfig
    backend_get: Callable[[str], list[float] | None]
    backend_set: Callable[[str, list[float], int], None]
    embed: Callable[[str], list[float]]
    emit_metric: Callable[[str, dict[str, Any]], None]
    model_name: str
    model_version: str

    def __post_init__(self) -> None:
        if self.config.hash_algo != "sha256":
            raise ValueError("hash_algo must be sha256 (rule r1)")
        if "model_version" not in self.config.key_components:
            raise ValueError("key_components must include model_version (rule r2)")
        if self.config.ttl_days < 1 or self.config.ttl_days > 365:
            raise ValueError("ttl_days must be in [1,365] (rule r3)")
        if not self.config.emit_hit_metric:
            raise ValueError("emit_hit_metric must be true (rule r4)")

    def _key(self, text: str) -> str:
        parts = []
        if "model_name" in self.config.key_components:
            parts.append(self.model_name)
        if "model_version" in self.config.key_components:
            parts.append(self.model_version)
        if "text" in self.config.key_components:
            parts.append(hashlib.sha256(text.encode("utf-8")).hexdigest())
        return ":".join(parts)

    def get_or_embed(self, text: str) -> list[float]:
        key = self._key(text)
        cached = self.backend_get(key)
        if cached is not None:
            self.emit_metric("embedding_cache.hit", {"model": self.model_name})
            return cached
        self.emit_metric("embedding_cache.miss", {"model": self.model_name})
        v = self.embed(text)
        ttl_seconds = self.config.ttl_days * 86400
        self.backend_set(key, v, ttl_seconds)
        return v
```

### `templates/cache-config.json`

```json
{
  "backend": "valkey",
  "hash_algo": "sha256",
  "key_components": [
    "model_name",
    "model_version",
    "text"
  ],
  "ttl_days": 90,
  "emit_hit_metric": true
}
```
