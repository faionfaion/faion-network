# Agent Integration — Hybrid Search Basics

## When to use
- Document corpus contains exact technical terms, product codes, model numbers, or names that semantic search misses.
- Domain is legal, medical, or compliance-heavy where precise phrase matching is required.
- User queries mix conceptual intent ("how to configure") with specific identifiers ("SK-8942").
- Pure vector search recall is below acceptable threshold on benchmark query set.
- System uses Qdrant, Weaviate, or Elasticsearch — all support hybrid search natively.

## When NOT to use
- Corpus is purely natural-language prose with no technical identifiers — pure semantic search suffices.
- Latency budget is very tight (< 100ms): hybrid adds BM25 scoring overhead; consider caching instead.
- Corpus is too small (< 500 documents) — BM25 gains are negligible at small scale.
- Already using a cross-encoder reranker over broad vector retrieval — the reranker compensates for keyword misses.

## Where it fails / limitations
- Alpha (semantic/keyword weight) requires per-domain tuning; a mistuned alpha underperforms pure vector search.
- BM25 does not handle synonyms or morphological variations — "configure" vs. "configuration" are different tokens.
- Score normalization across BM25 and cosine similarity is non-trivial; min-max normalization is sensitive to outlier scores in small result sets.
- Reciprocal Rank Fusion (RRF) treats all retrieval signals equally regardless of their quality — calibrating per-signal weights requires labeled data.
- In Qdrant/Weaviate native hybrid, the alpha parameter is global; no per-query dynamic alpha unless you call both backends separately and fuse client-side.
- BM25 index rebuild is required when documents are added incrementally — some vector DBs do not support live BM25 updates.

## Agentic workflow
The query analyst subagent inspects the incoming query for keywords (product codes, quoted phrases, rare terms) and computes a dynamic alpha. The retrieval subagent calls the vector DB's native hybrid search endpoint with the computed alpha. Results are passed to a reranker subagent for final scoring. The alpha selection decision and retrieval parameters are logged for continuous calibration.

### Recommended subagents
- `query-analyst` — Classifies query as semantic-heavy vs. keyword-heavy; returns alpha value 0.0–1.0.
- `hybrid-retriever` — Calls vector DB hybrid endpoint with computed alpha; returns top-k scored chunks.
- `alpha-calibrator` — Offline subagent that runs A/B evaluation across alpha values on labeled queries; updates stored alpha defaults.

### Prompt pattern
```python
# Dynamic alpha selection logic (embed in query-analyst subagent)
def compute_alpha(query: str) -> float:
    """1.0 = pure semantic, 0.0 = pure keyword."""
    if '"' in query:           return 0.2   # Quoted exact phrase
    if any(c.isdigit() for c in query): return 0.35  # Contains codes/numbers
    if len(query.split()) <= 3: return 0.5  # Short specific query
    return 0.7                              # Long conceptual query

# Qdrant native hybrid search
from qdrant_client.models import SparseVector, NamedSparseVector

results = qdrant_client.query_points(
    collection_name="docs",
    prefetch=[
        {"query": dense_embedding, "using": "dense", "limit": 20},
        {"query": SparseVector(indices=sparse_indices, values=sparse_values),
         "using": "sparse", "limit": 20},
    ],
    query=FusionQuery(fusion=Fusion.RRF),
    limit=10,
)
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `qdrant-client` | Native hybrid search via prefetch + RRF fusion | `pip install qdrant-client` / qdrant.tech/documentation |
| `rank_bm25` | Pure-Python BM25 for custom hybrid fusion | `pip install rank-bm25` / github.com/dorianbrown/rank_bm25 |
| `llama-index` | `QueryFusionRetriever` for BM25 + vector fusion | `pip install llama-index` / docs.llamaindex.ai |
| `langchain` | `EnsembleRetriever` with configurable weights | `pip install langchain` / python.langchain.com |
| `elasticsearch-py` | Elasticsearch `knn` + `query` hybrid natively | `pip install elasticsearch` / elastic.co/guide |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Qdrant | OSS / Cloud | Yes | Native sparse+dense hybrid via prefetch API; RRF built-in |
| Weaviate | OSS / Cloud | Yes | `hybrid()` query with alpha param; BM25 + vector natively |
| Elasticsearch | OSS / Cloud | Yes | `knn` + `query` clause; industry standard for keyword |
| OpenSearch | OSS | Yes | Same as Elasticsearch; AWS-managed variant |
| Pinecone | SaaS | Yes | Sparse-dense hybrid with sparse vectors (SPLADE compatible) |

## Templates & scripts
See `templates.md` for RRF fusion, Qdrant native hybrid, and dynamic alpha templates.

Client-side RRF fusion (provider-agnostic, under 30 lines):
```python
from collections import defaultdict

def rrf_fuse(rankings: list[list[str]], k: int = 60) -> list[tuple[str, float]]:
    """rankings: list of ranked doc-ID lists, one per retriever."""
    scores: dict[str, float] = defaultdict(float)
    for ranking in rankings:
        for rank, doc_id in enumerate(ranking):
            scores[doc_id] += 1.0 / (k + rank + 1)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

# Usage
vector_ids = [r.id for r in vector_results]
bm25_ids   = [r.id for r in bm25_results]
fused = rrf_fuse([vector_ids, bm25_ids])
```

## Best practices
- Start alpha at 0.5 and tune per domain using a labeled evaluation set of 50+ queries.
- Use RRF over linear score normalization by default — it is more robust to scale differences between BM25 and cosine scores.
- Apply BM25 domain-specific stop words; generic English stop words hurt technical corpora.
- Run vector search and BM25 independently in parallel, then fuse — do not rely on the database to do this unless the DB offers native hybrid.
- Normalize vectors before cosine scoring; un-normalized vectors produce incorrect similarity scores with dot-product indices.
- Log alpha used per query in production to build a calibration dataset.

## AI-agent gotchas
- Dynamic alpha must be computed before the retrieval call; an agent that decides alpha post-retrieval cannot change the result.
- BM25 scores are unbounded and distribution-dependent — never compare raw BM25 scores across different corpora or index configurations.
- When using `EnsembleRetriever` in LangChain, set `weights` explicitly; the default equal weighting is rarely optimal.
- Qdrant's sparse vector format requires SPLADE or BM25 pre-computed sparse encodings — you cannot pass raw text; tokenize and encode first.
- Human-in-loop checkpoint: when a query returns 0 results from both retrievers, escalate to a query-expansion step or human clarification rather than returning an empty answer.

## References
- https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf — Reciprocal Rank Fusion (original paper)
- https://qdrant.tech/articles/hybrid-search/ — Qdrant hybrid search guide
- https://python.langchain.com/docs/modules/data_connection/retrievers/ensemble/ — LangChain EnsembleRetriever
- https://en.wikipedia.org/wiki/Okapi_BM25 — BM25 algorithm reference
- https://arxiv.org/abs/2109.10086 — SPLADE: Sparse Lexical and Expansion Model for First Stage Ranking
