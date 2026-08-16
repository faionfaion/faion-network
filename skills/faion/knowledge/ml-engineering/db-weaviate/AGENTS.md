# Weaviate Vector Database

## Summary

**One-sentence:** Vector database for knowledge-graph + native hybrid (vector + BM25) workloads via GraphQL, with multi-vector multi-modal objects, scaling 10M–100M vectors self-hosted or via Weaviate Cloud.

**One-paragraph:** Weaviate combines vector + cross-reference graph + native BM25 in one query surface — eliminating client-side fusion code for hybrid pipelines. Python client v4 is required (v3 is incompatible). Classes define schema with `vectorizer` (or `none` for client-supplied vectors), `properties`, and `cross-references`. Multi-modal objects use named vectors. Replication factor and sharding are set at schema creation.

**Ефективно для:** RAG engineer building entity-linked knowledge graphs OR pipelines needing one-call hybrid search — closes the gap between maintaining vector + BM25 + graph as separate services.

## Applies If (ALL must hold)

- Knowledge-graph relationships required (entities with cross-references).
- Native hybrid (vector + BM25) needed without client-side fusion.
- GraphQL fits the team's API tooling.
- Self-hosted (Docker / K8s) at 10M–100M vectors OR Weaviate Cloud.

## Skip If (ANY kills it)

- Simple RAG prototype, no graph — Chroma or Qdrant are simpler.
- Team unfamiliar with GraphQL — Qdrant (REST/gRPC) is friendlier.
- Payload-filter perf at very high cardinality is the binding need — Qdrant outperforms.
- Cost-sensitive 1B+ managed — Pinecone / Milvus offer better per-vector pricing.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| weaviate-client | python pkg, **v4+** | `pip install weaviate-client` |
| Weaviate instance | URL + API key | Docker or Weaviate Cloud (WCS) |
| Schema definition | classes + properties + cross-refs | domain modelling |
| Vectorizer choice | `text2vec-openai` / `none` / `multi2vec-clip` | per use case |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/rag-engineer/db-comparison` | Why Weaviate over Qdrant. |
| `geek/ai/rag-engineer/hybrid-search-implementation` | Hybrid scoring semantics. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: v4 client, schema-first, native hybrid not client fusion, replication factor at schema, multi-vector for multi-modal | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for hybrid search response with alpha + sub-scores | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: v3 client mixed, manual fusion, no replication, missing cross-refs | ~700 |
| `content/04-procedure.xml` | deep | 6 steps: bring up → schema → cross-refs → upsert → hybrid query → backup | ~700 |
| `content/06-decision-tree.xml` | essential | Routes graph + hybrid + scale | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `schema-design` | sonnet | Domain modelling judgement. |
| `hybrid-tune-alpha` | sonnet | Recall/precision tradeoff with benchmarks. |
| `bulk-import` | haiku | I/O. |

## Templates

| File | Purpose |
|------|---------|
| `templates/weaviate_store.py` | WeaviateStore wrapper using client v4 with hybrid + cross-ref helpers. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[db-qdrant]] · [[db-comparison]] · [[hybrid-search-implementation]]

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` routes by knowledge-graph need, hybrid-search need, scale, and team GraphQL familiarity to Weaviate or an alternative.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/weaviate_store.py`

```python
"""WeaviateStore — minimal v4-client wrapper for hybrid + cross-ref queries."""
from __future__ import annotations

import weaviate
from weaviate.classes.config import Configure, Property, ReferenceProperty, DataType
from weaviate.classes.query import MetadataQuery


class WeaviateStore:
    def __init__(self, http_url: str, grpc_url: str, api_key: str | None = None) -> None:
        self.client = weaviate.connect_to_custom(
            http_host=http_url, http_port=8080, http_secure=False,
            grpc_host=grpc_url, grpc_port=50051, grpc_secure=False,
            auth_credentials=weaviate.auth.AuthApiKey(api_key) if api_key else None,
        )

    def ensure_class(self, name: str, replication_factor: int = 2) -> None:
        if not self.client.collections.exists(name):
            self.client.collections.create(
                name=name,
                properties=[
                    Property(name="title", data_type=DataType.TEXT),
                    Property(name="content", data_type=DataType.TEXT),
                ],
                references=[
                    ReferenceProperty(name="author", target_collection="Author"),
                ],
                replication_config=Configure.replication(factor=replication_factor),
            )

    def hybrid_search(self, class_name: str, query: str, alpha: float = 0.5, top_k: int = 5) -> dict:
        coll = self.client.collections.get(class_name)
        res = coll.query.hybrid(
            query=query, alpha=alpha, limit=top_k,
            return_metadata=MetadataQuery(score=True, explain_score=True),
        )
        hits = []
        for obj in res.objects:
            hits.append({
                "uuid": str(obj.uuid),
                "score": float(obj.metadata.score or 0.0),
                "vector_score": None,
                "bm25_score": None,
                "properties": dict(obj.properties),
            })
        return {
            "class_name": class_name, "query_type": "hybrid",
            "alpha": alpha, "top_k": top_k, "hits": hits,
        }

    def close(self) -> None:
        self.client.close()
```
