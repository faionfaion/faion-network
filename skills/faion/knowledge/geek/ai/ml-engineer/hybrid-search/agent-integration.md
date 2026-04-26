# Agent Integration — Hybrid Search

## When to use
- RAG pipeline serves queries that mix natural language and exact terms (product codes, error messages, legal statute numbers, names)
- Pure vector search precision is inadequate (< 75% relevant results in top-10) and queries include specific keywords that should match exactly
- Enterprise search over technical documentation where users alternate between concept searches and exact string lookups
- Production system where +15% precision gain justifies ~20% additional latency and complexity
- Replacing an existing BM25-only search with semantic capability without discarding keyword matching

## When NOT to use
- Corpus is < 1,000 documents — pure vector search is fast enough and simpler to operate
- All queries are conversational/semantic with no exact term requirements — pure vector search suffices; hybrid adds latency without benefit
- Latency budget is under 20ms — hybrid search (parallel BM25 + vector + fusion) typically costs 40-100ms
- Infrastructure is Elasticsearch-only — native kNN + BM25 in ES is effective without adding a second vector DB

## Where it fails / limitations
- Score normalization for linear fusion is non-trivial: BM25 scores are unbounded; vector scores are 0-1; without proper min-max or z-score normalization, one signal dominates
- Alpha tuning is dataset-specific: the optimal `alpha` value for `hybrid_score = alpha * vector + (1 - alpha) * bm25` on one corpus may perform poorly on another — requires empirical tuning
- RRF ignores actual score magnitudes: two documents with very different relevance scores but similar ranks get similar RRF scores, which may not reflect true quality
- Reranking top-100 adds 50-100ms and 5x cost compared to retrieval alone — only worth it when precision matters more than speed
- BM25 tokenization matters: if BM25 uses a standard English tokenizer but the corpus contains code, product codes, or non-English text, keyword matching degrades significantly
- Hybrid search from separate stores (manual RRF) has higher failure surface than native hybrid (Weaviate/Qdrant built-in) — two network calls, two failure modes

## Agentic workflow
A search agent receives a query, classifies it by type (semantic, keyword, mixed), and selects the appropriate fusion strategy. For mixed queries, the agent runs BM25 and vector search in parallel, applies RRF fusion, and optionally passes the top-100 candidates through a cross-encoder reranker to get the final top-10. The agent logs which retriever contributed to each final result for monitoring and tuning. For Weaviate/Qdrant deployments, the agent calls the native hybrid search endpoint in a single API call.

### Recommended subagents
- Query classifier subagent — detects if query contains exact terms (codes, quoted phrases, names) and returns `{type: "semantic"|"keyword"|"hybrid", alpha: float}`
- Hybrid retrieval tool — wraps the vector DB's native hybrid search or implements RRF fusion; returns ranked `{doc_id, score, retriever_source}` list

### Prompt pattern
```python
# Query-adaptive alpha selection
def get_alpha(query: str) -> float:
    has_quotes = '"' in query
    has_codes = any(c.isdigit() for c in query)
    is_short = len(query.split()) <= 3
    if has_quotes:
        return 0.2   # Strong keyword preference
    elif has_codes:
        return 0.3   # Keyword preference for product/ref codes
    elif is_short:
        return 0.5   # Balanced for short queries
    else:
        return 0.7   # Semantic preference for natural language
```

```python
# Qdrant native hybrid search
from qdrant_client import QdrantClient
from qdrant_client.models import Prefetch, FusionQuery, Fusion

def hybrid_search(client: QdrantClient, query: str, sparse_vector, dense_vector, top_k: int = 10):
    return client.query_points(
        collection_name="docs",
        prefetch=[
            Prefetch(query=sparse_vector, using="sparse", limit=100),
            Prefetch(query=dense_vector, using="dense", limit=100),
        ],
        query=FusionQuery(fusion=Fusion.RRF),
        limit=top_k,
    )
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `qdrant-client` | Native hybrid search (sparse + dense + RRF) | `pip install qdrant-client` |
| `weaviate-client` | Native hybrid search (BM25 + vector, alpha tuning) | `pip install weaviate-client` |
| `rank_bm25` | Pure Python BM25 implementation for manual fusion | `pip install rank-bm25` |
| `sentence-transformers` | Cross-encoder reranking models | `pip install sentence-transformers` |
| `elasticsearch` | kNN + BM25 hybrid (if already using ES) | `pip install elasticsearch` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Weaviate | SaaS + OSS | Yes — native hybrid | BM25 + vector; `alpha` parameter; single API call |
| Qdrant | SaaS + OSS | Yes — native hybrid | Sparse + dense prefetch + RRF; Rust performance |
| Pinecone | SaaS | Yes — native sparse-dense | Serverless; sparse index separate from dense |
| Elasticsearch | SaaS + OSS | Yes — kNN + BM25 | Good for existing ES infrastructure |
| MongoDB Atlas | SaaS | Yes — native hybrid | 8.0+; integrated with Atlas Search |
| Cohere Rerank | SaaS | Yes — REST | Cross-encoder reranker for post-fusion refinement |
| Jina Reranker | SaaS | Yes — REST | Fast; multilingual; good for diverse corpora |

## Templates & scripts
See `templates.md` for Weaviate, Qdrant, and manual RRF pipeline templates.

Inline: Reciprocal Rank Fusion (RRF) implementation (< 40 lines):

```python
from collections import defaultdict

def reciprocal_rank_fusion(
    result_lists: list[list[str]],
    k: int = 60,
    top_n: int = 10,
) -> list[tuple[str, float]]:
    """
    result_lists: list of ranked doc_id lists (best first per retriever)
    k: RRF constant (default 60 per original paper)
    Returns: sorted list of (doc_id, rrf_score) tuples
    """
    scores: dict[str, float] = defaultdict(float)
    for result_list in result_lists:
        for rank, doc_id in enumerate(result_list, start=1):
            scores[doc_id] += 1.0 / (k + rank)
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranked[:top_n]

# Usage: merge BM25 and vector results
bm25_ids = ["doc3", "doc1", "doc5", "doc2"]
vector_ids = ["doc1", "doc3", "doc7", "doc5"]
fused = reciprocal_rank_fusion([bm25_ids, vector_ids])
```

## Best practices
- Start with RRF as the default fusion method — it requires no score normalization, works across different score scales, and performs well out of the box; only switch to linear combination if RRF is measurably worse on your query set
- Use native hybrid search endpoints (Weaviate `alpha`, Qdrant `FusionQuery`) over manual two-call fusion — lower latency, fewer failure modes, less code
- Rerank top-100, not top-10 — the reranker is only as good as the candidates it receives; fetching top-10 for fusion and then reranking gives the reranker too little to work with
- Monitor retriever attribution: log which retriever contributed to each successful result — after 2 weeks, if BM25 contributes < 10% of final results, hybrid may not be needed for that query distribution
- Apply query-adaptive alpha: queries with quoted phrases or codes should use `alpha=0.2-0.3`; natural language questions should use `alpha=0.7`; implement a lightweight classifier to select dynamically
- Set BM25 parameters for your content: short document chunks need `b=0.3-0.5`; long documents need `b=0.75`; technical content needs higher `k1=1.5-2.0`

## AI-agent gotchas
- Score normalization required for linear fusion: BM25 scores for a corpus of 10K documents can range 0-30+; vector similarity scores range 0-1; mixing raw scores without normalization makes BM25 dominate entirely — always min-max normalize before linear combination
- Two parallel network calls double failure surface: if vector DB is slow but BM25 is fast, waiting for both adds tail latency; set a timeout on the slower call and fall back to the fast one's results alone
- Sparse vector generation for Qdrant hybrid: you need a sparse encoder (e.g., SPLADE, BM25 as sparse vectors) to generate the sparse representation — this is not the same as the BM25 library; ensure the sparse encoder is deployed and versioned
- Human-in-loop checkpoint: before switching from pure vector to hybrid search in production, run an A/B test on 5% of traffic and measure CTR or user satisfaction — latency + complexity cost must be justified by measurable quality gain

## References
- [Weaviate Hybrid Search Guide](https://weaviate.io/developers/weaviate/search/hybrid)
- [Qdrant Hybrid Search](https://qdrant.tech/articles/hybrid-search/)
- [Pinecone Sparse-Dense docs](https://docs.pinecone.io/docs/hybrid-search)
- [RRF original paper](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)
- [Optimizing RAG with Hybrid Search (Superlinked)](https://superlinked.com/vectorhub/articles/optimizing-rag-with-hybrid-search-reranking)
- [Elastic Hybrid Search](https://www.elastic.co/what-is/hybrid-search)
