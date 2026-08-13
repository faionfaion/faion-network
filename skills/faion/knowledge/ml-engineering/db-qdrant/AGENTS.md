# Qdrant Vector Database

## Summary

**One-sentence:** Self-hosted vector store for production RAG (41 QPS at 50M vectors), with payload-filter perf, quantization, and built-in sparse vectors for hybrid search without a separate engine.

**One-paragraph:** Qdrant runs as a single process (Docker / K8s); collections set `Distance` + HNSW config at creation. Scalar quantization halves RAM with negligible recall loss; binary quantization gives ~32x for high-dim embeddings. Built-in sparse vectors eliminate the BM25 sidecar in hybrid pipelines. Payload indexes accelerate `Filter` clauses to sub-millisecond at high cardinality. Snapshots are point-level and incremental.

**Ефективно для:** RAG engineer running self-hosted production RAG (1M+ vectors, hybrid search, payload filters) — closes the gap between Chroma's prototype-only ceiling and managed-only vendor lock-in.

## Applies If (ALL must hold)

- Production deployment, 1M+ vectors, self-hosted (Docker / K8s) or Qdrant Cloud.
- Payload filtering required alongside vector similarity.
- Hybrid (dense + sparse) search needed without a separate keyword engine.
- Snapshots / incremental backups required by the operations policy.

## Skip If (ANY kills it)

- Local prototype with <50k vectors — Chroma is simpler.
- Existing Postgres footprint with idle ops capacity — pgvector reuses infra.
- Need for fully managed SaaS without any infra ops — Qdrant Cloud or Pinecone.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| qdrant-client | python pkg | `pip install qdrant-client` |
| Qdrant instance | URL + API key | self-hosted or Qdrant Cloud |
| Collection config | Distance + HNSW m / ef_construct | tuned per corpus |
| Quantization plan | scalar / binary / none | RAM target |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/rag-engineer/db-comparison` | Why Qdrant over alternatives. |
| `geek/ai/rag-engineer/embedding-generation` | Embedding semantics for upsert. |
| `geek/ai/rag-engineer/hybrid-search-implementation` | Sparse-vector pattern. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: distance + HNSW at creation, payload indexes for filters, quantization tradeoffs, snapshot before schema change, named vectors for multi-modal | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for QdrantStore search response + upsert ack | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: missing payload index, mixed quantization, in-memory mode in prod, no snapshot before reindex | ~700 |
| `content/04-procedure.xml` | deep | 6 steps: install → collection create → payload indexes → upsert → quantize → snapshot | ~700 |
| `content/06-decision-tree.xml` | essential | Routes scale + hybrid + RAM budget | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `bootstrap` | haiku | Mechanical collection creation. |
| `tune-hnsw` | sonnet | Iterative benchmarking + judgement. |
| `quantization-decision` | sonnet | Recall vs RAM tradeoff. |

## Templates

| File | Purpose |
|------|---------|
| `templates/qdrant_store.py` | QdrantStore wrapper with collection bootstrap, batch upsert, filter, snapshot helpers. |
| `templates/qdrant-schema.json` | JSON Schema for QdrantStore search/upsert payloads. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-db-qdrant.py` | Verify search response schema; check payload index present per filter field; check snapshot before schema migration. | Pre-deploy + after each schema change. |

## Related

- [[db-chroma]] · [[db-weaviate]] · [[db-comparison]] · [[hybrid-search-implementation]]

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` routes by year-1 vectors, hybrid-search need, RAM budget, and ops capacity to Qdrant configuration (self-hosted vs Qdrant Cloud) with quantization choice.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/qdrant_store.py`

```python
"""
QdrantStore — minimal Qdrant wrapper: create collection, batch upsert, filtered search.

Usage:
    store = QdrantStore("documents", vector_size=1536)
    store.upsert([{"id": 1, "embedding": [...], "payload": {"text": "...", "source": "a.pdf"}}])
    results = store.search(query_embedding, top_k=10, must_match={"category": "technical"})
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    HnswConfigDiff,
    MatchValue,
    OptimizersConfigDiff,
    PointStruct,
    VectorParams,
)


@dataclass
class SearchResult:
    id: int | str
    score: float
    payload: Dict[str, Any]


class QdrantStore:
    def __init__(
        self,
        collection_name: str,
        vector_size: int = 1536,
        host: str = "localhost",
        port: int = 6333,
        batch_size: int = 100,
    ) -> None:
        self.collection_name = collection_name
        self.batch_size = batch_size
        self.client = QdrantClient(host=host, port=port)
        self._ensure_collection(vector_size)

    def _ensure_collection(self, vector_size: int) -> None:
        existing = [c.name for c in self.client.get_collections().collections]
        if self.collection_name not in existing:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
                hnsw_config=HnswConfigDiff(m=16, ef_construct=100),
                optimizers_config=OptimizersConfigDiff(indexing_threshold=20000),
                on_disk_payload=True,
            )

    def upsert(self, documents: List[Dict[str, Any]]) -> None:
        """documents: list of {id, embedding, payload}."""
        batch: List[PointStruct] = []
        for doc in documents:
            batch.append(PointStruct(
                id=doc["id"],
                vector=doc["embedding"],
                payload=doc.get("payload", {}),
            ))
            if len(batch) >= self.batch_size:
                self.client.upsert(collection_name=self.collection_name, points=batch)
                batch = []
        if batch:
            self.client.upsert(collection_name=self.collection_name, points=batch)

    def search(
        self,
        query_vector: List[float],
        top_k: int = 10,
        score_threshold: float = 0.0,
        must_match: Optional[Dict[str, Any]] = None,
    ) -> List[SearchResult]:
        search_filter = None
        if must_match:
            search_filter = Filter(must=[
                FieldCondition(key=k, match=MatchValue(value=v))
                for k, v in must_match.items()
            ])
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k,
            score_threshold=score_threshold,
            query_filter=search_filter,
            with_payload=True,
            with_vectors=False,
        )
        return [SearchResult(id=r.id, score=r.score, payload=r.payload or {}) for r in results]

    def snapshot(self) -> str:
        info = self.client.create_snapshot(collection_name=self.collection_name)
        return info.name
```

### `templates/qdrant-schema.json`

```json
{
  "_header": {
    "purpose": "JSON Schema for QdrantStore search response",
    "consumes": "QdrantStore.search() output",
    "produces": "pass/fail validation",
    "depends-on": "content/02-output-contract.xml",
    "token-budget-impact": "small"
  },
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "faion://db-qdrant/search.schema.json",
  "type": "object",
  "required": [
    "collection",
    "distance",
    "top_k",
    "hits",
    "payload_indexes_used"
  ],
  "properties": {
    "collection": {
      "type": "string",
      "minLength": 1
    },
    "distance": {
      "type": "string",
      "enum": [
        "Cosine",
        "Dot",
        "Euclid",
        "Manhattan"
      ]
    },
    "top_k": {
      "type": "integer",
      "minimum": 1,
      "maximum": 1000
    },
    "quantization": {
      "type": "string",
      "enum": [
        "none",
        "scalar",
        "binary"
      ]
    },
    "hits": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "id",
          "score",
          "payload"
        ]
      }
    },
    "payload_indexes_used": {
      "type": "array",
      "items": {
        "type": "string"
      }
    }
  }
}
```
