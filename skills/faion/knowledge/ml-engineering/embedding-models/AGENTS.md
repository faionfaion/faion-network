# Embedding Models

## Summary

**One-sentence:** Picks embedding model for a corpus class (general/code/multilingual) — pins model+version, handles Cohere input_type, OpenAI dimensions, Mistral/Voyage caveats, SentenceTransformer singleton.

**One-paragraph:** Each provider has quirks that, when missed, cost recall silently: OpenAI returns batches out of order, Cohere ignores input_type → 5–10% loss, Mistral truncates at 512 tokens, BGE-M3 sparse format mismatches dense DB clients. This methodology produces a `ModelSelector` artefact + bench harness that pins model name + version, applies provider tuning, and benchmarks Recall@10 against the domain set.

**Ефективно для:**

- New project — pick embedding model + provider.
- Migration between providers — confirm portability.
- Code corpora — Voyage-code-3, OpenAI text-embedding-3-large.
- Multilingual — Voyage, BGE-M3, Cohere embed-multilingual.
- High-storage-cost corpus — Matryoshka dim reduction with OpenAI v3.

## Applies If (ALL must hold)

- New project OR provider migration.
- Domain bench set available (≥50 pairs).
- Vector DB chosen with metric pinned.
- Named owner.

## Skip If (ANY kills it)

- Existing model meets recall target + no migration pending.
- No bench set.
- Single-provider lock-in for regulatory reasons.
- Greenfield prototype.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Candidate model catalog | YAML | platform |
| Domain bench set | JSONL | eval repo |
| Vector DB config (metric + dim) | YAML | platform |
| Token budget for bench | int | finops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[embedding-generation]]` | Calling convention. |
| `[[embedding-applications]]` | Pipeline that uses the choice. |
| `[[rag-bench-harness-template]]` | Bench. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 12 rules + run/skip terminals | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema for model-selection artefact | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with detector + repair | ~800 |
| `content/04-procedure.xml` | essential | 5-step: shortlist → tune → bench → pick winner → deploy | ~700 |
| `content/06-decision-tree.xml` | essential | Routes corpus class to model family | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `shortlist` | sonnet | Provider-aware judgment. |
| `run-bench` | haiku | Numeric. |
| `pick-winner` | opus | Multi-axis trade-off. |

## Templates

| File | Purpose |
|------|---------|
| `templates/embedding_pipeline.py` | Pipeline class with bench + selection. |
| `templates/model-selection.json` | Selection artefact skeleton. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-embedding-models.py` | Validate model-selection artefact | Pre-commit + CI |

## Related

- [[embedding-generation]]
- [[embedding-applications]]
- [[embedding-caching]]
- [[embedding-cost-optimization]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes corpus class (general/code/multilingual/legal-biomedical) to candidate family. The bench gate picks the winner within family.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/embedding_pipeline.py`

```python
"""EmbeddingPipeline — full pipeline: chunk → cache-check → batch embed.

Usage:
    config = EmbeddingConfig(model="text-embedding-3-large", chunk_size=500)
    pipeline = EmbeddingPipeline(config)
    embeddings = pipeline.process_document(long_text)  # list[list[float]]
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
import hashlib
import json
from pathlib import Path
from openai import OpenAI


@dataclass
class EmbeddingConfig:
    model: str = "text-embedding-3-large"
    dimensions: Optional[int] = None
    chunk_size: int = 500
    chunk_overlap: int = 50
    batch_size: int = 100
    cache_enabled: bool = True
    cache_dir: str = ".embedding_cache"


class EmbeddingPipeline:
    def __init__(self, config: EmbeddingConfig) -> None:
        self.config = config
        self.client = OpenAI()
        self.cache_dir = Path(config.cache_dir) if config.cache_enabled else None
        if self.cache_dir:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

    def process_document(self, text: str) -> list[list[float]]:
        """Chunk text → check cache → batch embed remaining → return all embeddings."""
        chunks = self._chunk(text)
        cached: dict[int, list[float]] = {}
        uncached: list[tuple[int, str]] = []

        for i, chunk in enumerate(chunks):
            hit = self._cache_get(chunk) if self.cache_dir else None
            if hit is not None:
                cached[i] = hit
            else:
                uncached.append((i, chunk))

        if uncached:
            indices, texts = zip(*uncached)
            new_embs = self._embed_batch(list(texts))
            for idx, emb in zip(indices, new_embs):
                cached[idx] = emb
                if self.cache_dir:
                    self._cache_set(chunks[idx], emb)

        return [cached[i] for i in range(len(chunks))]

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _chunk(self, text: str) -> list[str]:
        chunks, start = [], 0
        while start < len(text):
            end = start + self.config.chunk_size
            chunks.append(text[start:end].strip())
            start = end - self.config.chunk_overlap
        return [c for c in chunks if c]

    def _embed_batch(self, texts: list[str]) -> list[list[float]]:
        all_embs: list[list[float]] = []
        cfg = self.config
        for i in range(0, len(texts), cfg.batch_size):
            batch = texts[i : i + cfg.batch_size]
            kw: dict = {"input": batch, "model": cfg.model}
            if cfg.dimensions:
                kw["dimensions"] = cfg.dimensions
            r = self.client.embeddings.create(**kw)
            sorted_data = sorted(r.data, key=lambda x: x.index)
            all_embs.extend([e.embedding for e in sorted_data])
        return all_embs

    def _key(self, text: str) -> str:
        return hashlib.sha256(f"{self.config.model}:{text}".encode()).hexdigest()

    def _cache_get(self, text: str) -> Optional[list[float]]:
        path = self.cache_dir / f"{self._key(text)}.json"  # type: ignore[operator]
        if path.exists():
            return json.loads(path.read_text())
        return None

    def _cache_set(self, text: str, emb: list[float]) -> None:
        path = self.cache_dir / f"{self._key(text)}.json"  # type: ignore[operator]
        path.write_text(json.dumps(emb))
```

### `templates/model-selection.json`

```json
{
  "model_name": "text-embedding-3-large",
  "model_version": "2026-04",
  "provider": "openai",
  "corpus_class": "general",
  "dim": 512,
  "metric": "cosine",
  "mteb_retrieval_score": 0.668,
  "domain_recall10": 0.78,
  "provider_quirks": {
    "openai_dimensions": 512,
    "max_context_tokens": 8191
  }
}
```
