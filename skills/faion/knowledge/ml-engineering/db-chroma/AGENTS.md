# Chroma Vector Database

## Summary

**One-sentence:** Embedded SQLite/HNSW vector store for RAG prototyping with zero infrastructure and idempotent `get_or_create_collection` ingestion; single-process only.

**One-paragraph:** Chroma runs in-process (PersistentClient backed by SQLite + HNSW). Distance metric is set at collection creation and cannot be changed without recreating. IDs are strings (integers must be stringified). `get_or_create_collection` makes re-runs idempotent. Integrates directly with LangChain and LlamaIndex. Use Chroma for dev / eval / single-developer prototypes; promote to Qdrant or Pinecone before crossing 1M vectors, multi-tenant SaaS, or multi-process write workloads.

**Ефективно для:** Solopreneur prototyping a RAG pipeline locally — closes the gap between "open notebook" and a persistent vector store without Docker overhead.

## Applies If (ALL must hold)

- Single-developer prototype OR CI eval harness OR notebook-based research.
- Corpus < 1M vectors.
- Single-process write workload; no concurrent writers.
- Acceptable to migrate to a production vector store before scale-up.

## Skip If (ANY kills it)

- Production deployment with >1M vectors — load [[db-qdrant]] or [[db-weaviate]].
- Multi-tenant SaaS — Chroma lacks tenant isolation.
- High-concurrency writes — SQLite corrupts under concurrent writers.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| chromadb | python pkg | `pip install chromadb` |
| Persistence dir path | filesystem path | application config |
| Embedding function | callable or chromadb embedding fn | matches retrieval |
| Distance metric | "cosine" / "l2" / "ip" | decided once at collection creation |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/rag-engineer/embedding-generation` | Embedding function semantics. |
| `geek/ai/rag-engineer/db-comparison` | Why Chroma vs Qdrant/Weaviate. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: metric-at-creation, string IDs, get_or_create idempotent, single-process writes, persistence path | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for ChromaStore output: collection name, upsert ack, search hits with metadata | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: multi-process writes, integer IDs, metric change, missing persistence | ~700 |
| `content/04-procedure.xml` | medium | 5-step setup → embed → upsert → search → backup | ~600 |
| `content/06-decision-tree.xml` | essential | Routes scale + tenancy + concurrency to Chroma vs Qdrant vs pgvector | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `setup` | haiku | Mechanical client creation. |
| `bulk-upsert` | haiku | I/O. |
| `query-debug` | sonnet | Result inspection on poor recall. |

## Templates

| File | Purpose |
|------|---------|
| `templates/chroma_store.py` | ChromaStore wrapper with metric pinning, string IDs, idempotent upsert. |
| `templates/chroma-schema.json` | JSON Schema for ChromaStore search/upsert payloads. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-db-chroma.py` | Verify ChromaStore payload schema; check metric set; check IDs are strings. | After upsert / before commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[db-qdrant]] · [[db-weaviate]] · [[db-comparison]] · [[rag-architecture]]

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` routes by corpus size, tenancy, and concurrency to Chroma, Qdrant, Weaviate, or pgvector. Use it before instantiating a client so the scale-up path is explicit.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/chroma_store.py`

```python
"""
ChromaStore — minimal Chroma wrapper implementing upsert, search, delete.

Converts Chroma distances to similarity scores (1 - distance) for cosine space.

Usage:
    store = ChromaStore("documents", persist_dir="./chroma_db")
    store.upsert([{"id": "1", "embedding": [...], "content": "...", "metadata": {...}}])
    results = store.search(query_embedding, top_k=5)
    store.delete(["1", "2"])
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import chromadb


@dataclass
class SearchResult:
    id: str
    score: float      # similarity (1 - distance for cosine)
    content: str
    metadata: Dict[str, Any]


class ChromaStore:
    def __init__(
        self,
        collection_name: str,
        persist_dir: Optional[str] = "./chroma_db",
        distance: str = "cosine",  # cosine | l2 | ip
    ) -> None:
        if persist_dir:
            self._client = chromadb.PersistentClient(path=persist_dir)
        else:
            self._client = chromadb.Client()
        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": distance},
        )
        self._distance = distance

    def upsert(self, documents: List[Dict[str, Any]]) -> None:
        """documents: list of {id, embedding, content, metadata}."""
        self._collection.upsert(
            ids=[str(d["id"]) for d in documents],
            embeddings=[d["embedding"] for d in documents],
            documents=[d.get("content", "") for d in documents],
            metadatas=[d.get("metadata", {}) for d in documents],
        )

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        where: Optional[Dict] = None,
    ) -> List[SearchResult]:
        kwargs: Dict[str, Any] = {
            "query_embeddings": [query_embedding],
            "n_results": top_k,
            "include": ["documents", "metadatas", "distances"],
        }
        if where:
            kwargs["where"] = where
        r = self._collection.query(**kwargs)
        results = []
        for i in range(len(r["ids"][0])):
            dist = r["distances"][0][i]
            score = 1.0 - dist if self._distance == "cosine" else -dist
            results.append(SearchResult(
                id=r["ids"][0][i],
                score=score,
                content=r["documents"][0][i],
                metadata=r["metadatas"][0][i],
            ))
        return results

    def delete(self, ids: List[str]) -> None:
        self._collection.delete(ids=[str(i) for i in ids])
```

### `templates/chroma-schema.json`

```json
{
  "_header": {
    "purpose": "JSON Schema for ChromaStore search response",
    "consumes": "ChromaStore.search() output",
    "produces": "pass/fail validation",
    "depends-on": "content/02-output-contract.xml",
    "token-budget-impact": "small"
  },
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "faion://db-chroma/search.schema.json",
  "type": "object",
  "required": [
    "collection",
    "metric",
    "top_k",
    "hits"
  ],
  "properties": {
    "collection": {
      "type": "string",
      "minLength": 1
    },
    "metric": {
      "type": "string",
      "enum": [
        "cosine",
        "l2",
        "ip"
      ]
    },
    "top_k": {
      "type": "integer",
      "minimum": 1,
      "maximum": 1000
    },
    "hits": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "id",
          "score",
          "payload"
        ],
        "properties": {
          "id": {
            "type": "string",
            "minLength": 1
          },
          "score": {
            "type": "number"
          },
          "payload": {
            "type": "object"
          }
        }
      }
    }
  }
}
```
