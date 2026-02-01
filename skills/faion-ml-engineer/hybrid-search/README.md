# Hybrid Search for RAG Systems

Combining keyword-based (sparse) and semantic (dense) search to maximize retrieval quality in RAG applications.

## Why Hybrid Search

| Approach | Strengths | Weaknesses |
|----------|-----------|------------|
| **BM25 (Sparse)** | Exact matches, keywords, codes, names | Misses synonyms, context, intent |
| **Vector (Dense)** | Semantic similarity, synonyms, context | Misses exact terms, rare words, codes |
| **Hybrid** | Best of both: precision + semantic understanding | Slightly higher latency (~20%) |

**2025-2026 Benchmarks:**
- BM25 alone: 62% relevant documents in top 10
- Semantic alone: 71% relevant documents in top 10
- Hybrid + reranking: 87% relevant documents in top 10
- NDCG@10 improvement: +42% over pure vector search

## When to Use Hybrid Search

### Strong Candidates

| Use Case | Why Hybrid Helps |
|----------|------------------|
| Enterprise search | Mix of exact codes, names, and natural language |
| Legal/compliance | Exact statute references + semantic context |
| Technical documentation | Code snippets + conceptual explanations |
| E-commerce | Product codes + natural descriptions |
| Medical records | ICD codes + clinical narratives |
| Customer support | Ticket IDs + issue descriptions |

### When Pure Vector May Suffice

- Creative content search (poems, stories)
- Conversational queries only
- No exact match requirements
- Small corpus (<1000 documents)

### When Pure BM25 May Suffice

- Exact phrase search only
- Log file searching
- Code search (specific function names)
- Extremely latency-sensitive (<10ms)

## Core Concepts

### Sparse vs Dense Representations

```
Query: "Python async database connection"

SPARSE (BM25):
- Tokenizes: ["python", "async", "database", "connection"]
- Matches: Exact token occurrences
- Scores: TF-IDF / BM25 formula

DENSE (Vector):
- Embeds: query → [0.12, -0.45, 0.78, ...] (768-1536 dims)
- Matches: Cosine similarity in embedding space
- Scores: 0.0 to 1.0 similarity
```

### BM25 Parameters

| Parameter | Default | Effect |
|-----------|---------|--------|
| **k1** | 1.5 | Term frequency saturation (higher = more weight to repeated terms) |
| **b** | 0.75 | Document length normalization (0 = none, 1 = full) |

Tuning guidance:
- Short documents: Lower b (0.3-0.5)
- Long documents: Higher b (0.75-0.9)
- Technical content: Higher k1 (1.5-2.0)
- General content: k1 around 1.2

### Fusion Methods

#### Reciprocal Rank Fusion (RRF)

**Formula:** `RRF_score(d) = SUM(1 / (k + rank_i(d)))` where k = 60 (default)

**Advantages:**
- No score normalization needed
- Works across different score scales
- Robust, requires no tuning
- Default choice for most applications

**Limitations:**
- Cannot weight one retriever over another
- Ignores actual score magnitudes

#### Weighted Linear Combination

**Formula:** `hybrid_score = alpha * vector_score + (1 - alpha) * bm25_score`

| Alpha | Interpretation |
|-------|----------------|
| 0.0 | Pure BM25 |
| 0.3 | Favor keywords |
| 0.5 | Balanced |
| 0.7 | Favor semantic |
| 1.0 | Pure vector |

**Advantages:**
- Fine-grained control
- Can outperform RRF with proper tuning
- Adjustable per query type

**Limitations:**
- Requires score normalization
- Sensitive to tuning
- Dataset-specific optimal values

#### Query-Adaptive Alpha

```python
def determine_alpha(query: str) -> float:
    """Dynamically select alpha based on query characteristics."""
    has_quotes = '"' in query          # Exact phrase
    has_codes = any(c.isdigit() for c in query)  # Product/ref codes
    is_short = len(query.split()) <= 3
    has_technical = any(t in query.lower() for t in ['error', 'exception', 'api'])

    if has_quotes:
        return 0.2  # Strong keyword preference
    elif has_codes:
        return 0.3  # Keyword preference for codes
    elif has_technical:
        return 0.4  # Balanced with keyword lean
    elif is_short:
        return 0.5  # Balanced
    else:
        return 0.7  # Semantic for natural language
```

### Reranking

**Purpose:** Refine hybrid results using a more powerful cross-encoder model.

**Architecture:**
```
Query + Docs → Hybrid Retrieval (top 100) → Reranker → Final Results (top 10)
```

**Popular Rerankers:**

| Model | Speed | Quality | Use Case |
|-------|-------|---------|----------|
| Cohere Rerank | Fast | High | Production API |
| bge-reranker-v2-m3 | Medium | High | Self-hosted |
| cross-encoder/ms-marco | Slow | Very High | Offline, batch |
| Jina Reranker | Fast | High | Multilingual |

**Trade-offs:**
- Reranking top-100 adds ~50-100ms latency
- Precision improvement: +15% on average
- Cost: 5x more than retrieval alone

## Vector Database Selection

| Database | Hybrid Support | Best For |
|----------|---------------|----------|
| **Weaviate** | Native (built-in BM25 + vector) | Production, graphs |
| **Qdrant** | Native (sparse + dense vectors) | Self-hosted production |
| **Pinecone** | Native (sparse-dense) | Managed, serverless |
| **Elasticsearch** | Native (kNN + BM25) | Existing ES infrastructure |
| **pgvector** | Manual (combine with pg_trgm) | PostgreSQL projects |
| **Milvus** | Native (2.4+) | Large scale |
| **MongoDB Atlas** | Native (8.0+) | MongoDB ecosystem |

### Quick Comparison

```
Latency (p95, 1M docs):
- Weaviate: 45ms hybrid
- Qdrant: 40ms hybrid
- Pinecone: 50ms hybrid
- Elasticsearch: 60ms hybrid

Memory (per 1M vectors, 768d):
- Qdrant: ~4GB
- Weaviate: ~5GB
- Pinecone: Managed
- pgvector: ~3GB (HNSW)
```

## Performance Optimization

### Latency Budget

| Component | Typical Latency | Optimization |
|-----------|----------------|--------------|
| BM25 | 10-50ms | Index optimization, sharding |
| Vector search | 50-200ms | HNSW params, quantization |
| Fusion | 1-5ms | Pre-compute where possible |
| Reranking | 50-100ms | Batch, limit candidates |
| **Total** | 100-350ms | Set SLO, optimize bottleneck |

### Scaling Strategies

1. **Vertical:** More RAM, faster SSD, GPU for reranking
2. **Horizontal:** Sharding by document type/date
3. **Caching:** Cache frequent queries (15-min TTL typical)
4. **Async:** Parallel BM25 and vector search
5. **Quantization:** Reduce vector dimensions (768 → 384)

## LLM Usage Tips

### For Implementation

1. **Start with RRF** - No tuning required, works well out of the box
2. **Add reranking later** - Only if precision is insufficient
3. **Use native hybrid** - Weaviate/Qdrant/Pinecone built-in beats manual
4. **Benchmark early** - Measure before optimizing

### For Evaluation

```python
# Key metrics to track
metrics = {
    "ndcg@10": "Ranking quality",
    "recall@100": "Coverage before reranking",
    "precision@10": "Final result quality",
    "mrr": "Position of first relevant result",
    "latency_p95": "User experience",
}
```

### For Production

1. **Monitor alpha effectiveness** - Log which alpha values produce clicks
2. **A/B test fusion methods** - RRF vs linear on real traffic
3. **Track retrieval attribution** - Which retriever contributed to successful results
4. **Set up fallbacks** - If vector search fails, fallback to BM25

## Common Pitfalls

| Pitfall | Impact | Solution |
|---------|--------|----------|
| Not normalizing scores for linear fusion | Inconsistent ranking | Min-max or z-score normalization |
| Same alpha for all queries | Suboptimal for diverse queries | Query-adaptive alpha |
| Reranking too few candidates | Missing good results | Rerank top 100, not top 10 |
| Ignoring BM25 tokenization | Poor keyword matching | Match tokenizer to content language |
| Over-fetching for fusion | High latency | Fetch 2-3x final k, not more |

## Further Reading

- [Weaviate Hybrid Search Guide](https://weaviate.io/developers/weaviate/search/hybrid)
- [Qdrant Hybrid Search](https://qdrant.tech/articles/hybrid-search/)
- [Pinecone Sparse-Dense](https://docs.pinecone.io/docs/hybrid-search)
- [Elastic Hybrid Search](https://www.elastic.co/what-is/hybrid-search)
- [RRF Paper](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)
- [Optimizing RAG with Hybrid Search](https://superlinked.com/vectorhub/articles/optimizing-rag-with-hybrid-search-reranking)
- [MongoDB Hybrid Search](https://www.mongodb.com/resources/products/capabilities/hybrid-search)
- [Meilisearch Hybrid RAG](https://www.meilisearch.com/blog/hybrid-search-rag)

## Files in This Directory

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Implementation, tuning, evaluation checklists |
| [examples.md](examples.md) | Code examples for various vector DBs |
| [templates.md](templates.md) | Pipeline and configuration templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for implementation and debugging |

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Hybrid search setup | sonnet | Search architecture |
| Weight optimization | sonnet | Parameter tuning |
| Performance comparison | sonnet | Evaluation |
