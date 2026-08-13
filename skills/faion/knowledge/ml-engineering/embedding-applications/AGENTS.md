# Embedding Applications

## Summary

**One-sentence:** End-to-end embedding pipeline — MTEB-anchored model selection plus domain benchmarking, batched insertion, normalized cosine, model-version metadata, Recall@10 quality gate.

**One-paragraph:** Pick the wrong embedding model and the whole RAG underperforms; pick right but skip normalization or batching and cost/latency explode. This methodology produces a multi-agent embedding pipeline: model selection (MTEB retrieval score + 50–200 domain pairs), embedding generation (batched + backoff), vector DB insertion (normalized + version metadata), and a Recall@10 quality gate that blocks promotion to production.

**Ефективно для:**

- New RAG project обирати embedding model — MTEB ≠ retrieval rank.
- Domain-specific corpus (legal, biomedical, code) — custom bench mandatory.
- Cross-provider migration (OpenAI ↔ Cohere ↔ Voyage ↔ local).
- Re-indexing trigger при model deprecation.
- Cost/quality trade-off через Matryoshka dims.

## Applies If (ALL must hold)

- New RAG pipeline OR model migration.
- 50–200 labeled domain query/doc pairs available.
- Vector DB with cosine support.
- Named owner.

## Skip If (ANY kills it)

- General-purpose corpus already well-served by ada-002 baseline.
- &lt;50 labeled domain pairs (cannot bench reliably).
- Single-model lock-in for legal reasons.
- No re-indexing budget.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Domain corpus sample | JSONL | warehouse |
| Labeled query/doc pairs (50–200) | JSONL | eval repo |
| Candidate model catalog | YAML | platform |
| Vector DB client (Qdrant/pgvector/Weaviate) | client | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[embedding-models]]` | Provider-specific rules. |
| `[[embedding-generation]]` | Batching + normalization rules. |
| `[[rag-bench-harness-template]]` | Bench harness. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules + run/skip terminals | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for embedding-pipeline-config | ~700 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns with detector + repair | ~800 |
| `content/04-procedure.xml` | essential | 5-step: shortlist → domain-bench → wire batched → quality-gate → deploy | ~800 |
| `content/06-decision-tree.xml` | essential | Routes domain to model class | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `shortlist-models` | sonnet | MTEB filter + domain knowledge. |
| `run-domain-bench` | haiku | Mechanical metric compute. |
| `quality-gate-review` | opus | Cross-metric synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/embedding_pipeline.py` | Pipeline class with model selection + bench + insert + gate. |
| `templates/embedding-pipeline-config.json` | Config skeleton. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-embedding-applications.py` | Validate embedding-pipeline-config | Pre-commit + CI |

## Related

- [[embedding-models]]
- [[embedding-generation]]
- [[embedding-cost-optimization]]
- [[rag-bench-harness-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes domain class to candidate model set (general / code / multilingual / legal-biomedical) and gates promotion on Recall@10 threshold.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/embedding_pipeline.py`

```python
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class EmbeddingPipelineConfig:
    model_name: str
    model_version: str
    provider: str
    batch_size: int = 256
    normalize: bool = True
    metric: str = "cosine"
    domain_bench_path: str = ""
    recall10_threshold: float = 0.7
    vector_metadata_fields: tuple[str, ...] = ("model_name", "model_version", "created_at")


def _normalize(v: list[float]) -> list[float]:
    n = math.sqrt(sum(x * x for x in v))
    if n < 1e-9:
        raise ValueError("zero-length vector (rule r3)")
    return [x / n for x in v]


@dataclass
class EmbeddingPipeline:
    config: EmbeddingPipelineConfig
    embed_batch: Callable[[list[str]], list[list[float]]]
    db_upsert: Callable[[list[dict]], None]
    db_get_config: Callable[[], dict]
    bench_recall10: Callable[[str, EmbeddingPipelineConfig], float]

    def __post_init__(self) -> None:
        if self.config.batch_size < 32 or self.config.batch_size > 2048:
            raise ValueError("batch_size out of [32,2048] (rule r5)")
        if self.config.metric == "cosine" and not self.config.normalize:
            raise ValueError("cosine metric requires normalize=true (rule r3)")
        for fld in ("model_name", "model_version"):
            if fld not in self.config.vector_metadata_fields:
                raise ValueError(f"vector_metadata_fields missing {fld} (rule r7)")

    def ingest(self, docs: list[dict]) -> dict[str, Any]:
        # rule r6: schema check before upsert
        cfg = self.db_get_config()
        if cfg.get("metric") != self.config.metric:
            raise ValueError(f"DB metric {cfg.get('metric')} != config {self.config.metric} (rule r6)")
        inserted = 0
        for start in range(0, len(docs), self.config.batch_size):
            batch = docs[start : start + self.config.batch_size]
            vectors = self.embed_batch([d["text"] for d in batch])
            if self.config.normalize:
                vectors = [_normalize(v) for v in vectors]
            rows = [
                {
                    "id": d["id"],
                    "vector": v,
                    "metadata": {
                        "model_name": self.config.model_name,
                        "model_version": self.config.model_version,
                        "created_at": d.get("created_at"),
                    },
                }
                for d, v in zip(batch, vectors, strict=True)
            ]
            self.db_upsert(rows)
            inserted += len(rows)
        return {"inserted": inserted}

    def quality_gate(self) -> dict[str, Any]:
        # rule r4: gate on Recall@10
        recall = self.bench_recall10(self.config.domain_bench_path, self.config)
        ok = recall >= self.config.recall10_threshold
        return {"recall10": recall, "promoted": ok}
```

### `templates/embedding-pipeline-config.json`

```json
{
  "model_name": "text-embedding-3-large",
  "model_version": "2026-04",
  "provider": "openai",
  "batch_size": 256,
  "normalize": true,
  "metric": "cosine",
  "domain_bench_path": "git://<repo>/eval/embed-bench.jsonl",
  "recall10_threshold": 0.7,
  "vector_metadata_fields": [
    "model_name",
    "model_version",
    "created_at"
  ]
}
```
