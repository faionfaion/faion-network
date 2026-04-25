# Agent Integration — Hybrid Search Implementation

## When to use
- RAG over technical documentation where exact identifiers (function names, error codes, version numbers) matter alongside semantic meaning
- Legal, medical, or compliance corpora where specific terminology must match exactly
- Search over short queries (1-3 words) where semantic vectors alone underperform BM25
- Multilingual corpora where the query language may differ from document language (vector handles cross-lingual, BM25 handles same-language exact match)
- Upgrading an existing keyword-only search system to add semantic understanding without full replacement

## When NOT to use
- Purely conversational or conceptual queries with no exact-match requirements — dense-only retrieval is simpler and sufficient
- Very small corpora (<5K documents) where BM25 overhead is not justified
- Real-time indexing of streaming documents where BM25 corpus statistics must be constantly rebuilt
- Latency-critical paths where running two retrieval pipelines in parallel doubles P99 latency beyond SLA

## Where it fails / limitations
- Alpha tuning (dense vs sparse weight) is data-dependent; wrong alpha degrades results worse than single-method search — must be measured on a labeled eval set
- BM25 tokenization is language-specific; the default English tokenizer produces poor scores for CJK, Arabic, or other non-whitespace-delimited languages
- RRF (Reciprocal Rank Fusion) discards absolute scores, which can surface low-confidence results from both methods at the same rank
- Pinecone's sparse-dense hybrid requires training `BM25Encoder` on the full corpus before ingestion; corpus size changes invalidate the encoder
- Qdrant's native hybrid (prefetch + FusionQuery) requires sparse vectors to be pre-computed outside Qdrant — there is no built-in BM25 tokenizer
- Elasticsearch hybrid scoring is sensitive to BM25 score scale vs cosine similarity scale; naive linear combination requires per-corpus normalization

## Agentic workflow
An indexing agent builds both a dense index (embeddings) and a sparse index (BM25 on tokenized corpus or Qdrant sparse vectors). A query-routing agent inspects query characteristics — presence of quoted strings, numeric codes, query length — and selects the alpha value dynamically or uses a fixed config. Retrieval agents run both search paths in parallel, fuse results using RRF, and pass the top-K merged list to generation. Alpha tuning is a human decision based on offline eval results.

### Recommended subagents
- `faion-sdd-executor-agent` — builds both indexes and configures fusion method
- Custom routing agent — classifies query type and selects alpha before calling retrieval

### Prompt pattern
```
You are a hybrid search agent. Given: query, dense_index, sparse_index, alpha.
Steps:
1. Embed query → dense_results (top 20).
2. Tokenize query → BM25 scores → sparse_results (top 20).
3. Apply RRF fusion with k=60.
4. Return top-10 fused results with scores and provenance (which method contributed).
```

```
You are a query classifier. Given: query string.
Classify the query:
- "exact": contains quotes, codes, version numbers → alpha=0.2 (favor BM25)
- "semantic": long natural language question → alpha=0.8 (favor dense)
- "balanced": mixed → alpha=0.5
Return: {"type": "...", "alpha": 0.X}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `rank-bm25` | Pure-Python BM25 implementation | `pip install rank-bm25` / [GitHub](https://github.com/dorianbrown/rank_bm25) |
| `pinecone-text` | Sparse BM25 encoder for Pinecone | `pip install pinecone-text` / [docs](https://github.com/pinecone-io/pinecone-text) |
| `elasticsearch` (Python) | Full-text + vector hybrid in ES | `pip install elasticsearch` / [docs](https://www.elastic.co/guide/en/elasticsearch/client/python-api/) |
| `qdrant-client` | Prefetch + FusionQuery for hybrid | `pip install qdrant-client` / [docs](https://qdrant.tech/articles/hybrid-search/) |
| `weaviate-client` | Built-in hybrid search with alpha | `pip install weaviate-client` / [docs](https://weaviate.io/developers/weaviate/search/hybrid) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Weaviate (OSS/Cloud) | Both | Yes | Cleanest native hybrid API; alpha param built-in |
| Pinecone | SaaS | Yes | Requires `pinecone-text` BM25Encoder pre-fitted on corpus |
| Qdrant (OSS/Cloud) | Both | Yes | Sparse vectors must be pre-computed; FusionQuery for RRF |
| Elasticsearch | OSS/SaaS | Yes — REST | script_score approach; requires careful score normalization |
| OpenSearch | OSS | Yes — REST | ES-compatible hybrid search with neural plugin |
| Typesense | OSS | Yes | Simpler than ES; hybrid requires v0.25+ |

## Templates & scripts
See `templates.md` for the `HybridSearchService` class with RRF and linear fusion.

Inline RRF fusion (standalone, no DB dependency):
```python
from collections import defaultdict

def rrf_fusion(vector_results, keyword_results, k=60):
    """vector_results, keyword_results: list of (doc_id, score) tuples, ranked."""
    scores = defaultdict(float)
    for rank, (doc_id, _) in enumerate(vector_results):
        scores[doc_id] += 1.0 / (k + rank + 1)
    for rank, (doc_id, _) in enumerate(keyword_results):
        scores[doc_id] += 1.0 / (k + rank + 1)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)
```

## Best practices
- Default to RRF over linear combination: RRF is robust to scale differences between BM25 and cosine scores, requires no normalization
- Always fetch 2-3x more candidates from each method than the final top-K before fusion — fusion can promote documents not in top-10 of either method alone
- Build a labeled evaluation set (50-200 query/relevant-doc pairs) before tuning alpha — intuition about the right alpha is usually wrong
- For Weaviate, `HybridFusion.RELATIVE_SCORE` generally outperforms `RANKED` for corpora with high score variance
- Use the `determine_alpha` pattern (detect quotes, codes, query length) to route query types automatically rather than one global alpha
- For Elasticsearch, normalize BM25 scores with `/max(bm25_scores)` and cosine similarity is already [0,1] before linear combination

## AI-agent gotchas
- Agents must fit the BM25Encoder on the full corpus before any ingestion — fitting after partial ingestion produces incorrect IDF weights
- Pinecone sparse vector format is `{"indices": [...], "values": [...]}` — agents must not confuse it with Qdrant's `SparseVector(indices=..., values=...)`
- Weaviate's alpha=0 is pure BM25, alpha=1 is pure vector — the opposite convention from some papers where alpha=0 means full semantic; always verify the client's convention
- RRF k=60 is a heuristic that works well for document search; for code search with hundreds of results, k=30 may be better — agents should expose k as a config param
- Multi-language corpora need per-language tokenizers in BM25; a single English BM25 tokenizer on a mixed corpus degrades non-English recall
- Running two retrieval paths has additive latency in serial mode; agents should use `asyncio.gather` or thread-pool to parallelize dense and sparse searches

## References
- [Reciprocal Rank Fusion (Cormack et al. 2009)](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)
- [Weaviate Hybrid Search Docs](https://weaviate.io/developers/weaviate/search/hybrid)
- [Pinecone Hybrid Search](https://docs.pinecone.io/docs/hybrid-search)
- [Qdrant Hybrid Search](https://qdrant.tech/articles/hybrid-search/)
- [Elasticsearch Hybrid](https://www.elastic.co/guide/en/elasticsearch/reference/current/knn-search.html)
