# M-RAG-004: Retrieval Strategies

## Overview

Retrieval strategies determine how relevant documents are found and ranked. Beyond basic similarity search, techniques include hybrid search, reranking, query expansion, and multi-stage retrieval. The right strategy dramatically impacts RAG quality.

**When to use:** Optimizing RAG retrieval quality, building production search systems, or when basic vector search is insufficient.

## Core Concepts

### 1. Retrieval Methods

| Method | Description | Precision | Recall |
|--------|-------------|-----------|--------|
| **Vector (Dense)** | Embedding similarity | High | Medium |
| **Keyword (Sparse)** | BM25, TF-IDF | Medium | High |
| **Hybrid** | Vector + Keyword | High | High |
| **Multi-stage** | Coarse → Fine | Very High | High |

### 2. Ranking Signals

| Signal | Source | Weight |
|--------|--------|--------|
| **Semantic similarity** | Vector distance | Primary |
| **Keyword match** | BM25 score | Secondary |
| **Recency** | Timestamp | Contextual |
| **Popularity** | Click/usage data | Boost |
| **Authority** | Source credibility | Boost |
| **Reranker score** | Cross-encoder | Final |

### 3. Retrieval Pipeline

```
Query → Expansion → Retrieval → Fusion → Rerank → Filter → Output
  ↓         ↓           ↓          ↓        ↓        ↓
Original  Synonyms   Vector+    RRF/     Cross-   Business
Query     Related    Keyword    Weighted  encoder  Rules
```

## Best Practices

### 1. Use Hybrid Search

```python
def hybrid_search(
    query: str,
    query_embedding: list,
    vector_store,
    keyword_store,
    alpha: float = 0.7,  # Vector weight
    k: int = 10
) -> list:
    """Combine dense and sparse retrieval."""

    # Dense retrieval (embeddings)
    vector_results = vector_store.search(
        vector=query_embedding,
        limit=k * 3
    )

    # Sparse retrieval (BM25)
    keyword_results = keyword_store.search(
        query=query,
        limit=k * 3
    )

    # Reciprocal Rank Fusion
    fused = reciprocal_rank_fusion(
        [vector_results, keyword_results],
        k=60  # RRF constant
    )

    # Or weighted linear combination
    # fused = weighted_fusion(vector_results, keyword_results, alpha)

    return fused[:k]

def reciprocal_rank_fusion(result_lists: list, k: int = 60) -> list:
    """Combine rankings using RRF."""

    scores = {}

    for results in result_lists:
        for rank, doc in enumerate(results, 1):
            doc_id = doc.id
            if doc_id not in scores:
                scores[doc_id] = {"doc": doc, "score": 0}
            scores[doc_id]["score"] += 1 / (k + rank)

    # Sort by combined score
    sorted_docs = sorted(
        scores.values(),
        key=lambda x: x["score"],
        reverse=True
    )

    return [item["doc"] for item in sorted_docs]
```

### 2. Apply Reranking

```python
from sentence_transformers import CrossEncoder

class Reranker:
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-12-v2"):
        self.model = CrossEncoder(model_name)

    def rerank(
        self,
        query: str,
        documents: list,
        top_k: int = None
    ) -> list:
        """Rerank documents using cross-encoder."""

        # Create query-document pairs
        pairs = [(query, doc.text) for doc in documents]

        # Score all pairs
        scores = self.model.predict(pairs)

        # Sort by score
        scored_docs = [
            {"doc": doc, "score": score}
            for doc, score in zip(documents, scores)
        ]
        scored_docs.sort(key=lambda x: x["score"], reverse=True)

        if top_k:
            scored_docs = scored_docs[:top_k]

        return scored_docs

# Usage in RAG pipeline
def retrieve_and_rerank(query: str, initial_k: int = 50, final_k: int = 5):
    # Stage 1: Fast retrieval (larger set)
    candidates = hybrid_search(query, embed(query), k=initial_k)

    # Stage 2: Accurate reranking (smaller set)
    reranked = reranker.rerank(query, candidates, top_k=final_k)

    return reranked
```

### 3. Expand Queries

```python
def expand_query(query: str, llm) -> list[str]:
    """Generate query variations for better recall."""

    prompt = f"""
    Generate 3 alternative search queries that capture the same intent.
    Focus on different phrasings and related terms.

    Original query: "{query}"

    Return as JSON array of strings.
    """

    response = llm.invoke(prompt)
    variations = json.loads(response)

    return [query] + variations

def multi_query_retrieval(
    query: str,
    vector_store,
    k_per_query: int = 5
) -> list:
    """Retrieve using multiple query variations."""

    queries = expand_query(query, llm)
    all_results = []

    for q in queries:
        embedding = embed(q)
        results = vector_store.search(embedding, limit=k_per_query)
        all_results.extend(results)

    # Deduplicate and rank
    unique_results = deduplicate_by_id(all_results)
    return unique_results
```

## Common Patterns

### Pattern 1: Multi-Stage Retrieval

```python
class MultiStageRetriever:
    def __init__(self, vector_store, reranker, llm):
        self.vector_store = vector_store
        self.reranker = reranker
        self.llm = llm

    def retrieve(self, query: str, final_k: int = 5) -> list:
        """Multi-stage retrieval pipeline."""

        # Stage 1: Query understanding
        enhanced_query = self._enhance_query(query)

        # Stage 2: Initial retrieval (fast, high recall)
        candidates = self._initial_retrieval(enhanced_query, k=100)

        # Stage 3: Pre-filtering (cheap filters)
        filtered = self._pre_filter(candidates, query)

        # Stage 4: Reranking (accurate, slower)
        reranked = self.reranker.rerank(query, filtered, top_k=20)

        # Stage 5: Diversity sampling
        diverse = self._ensure_diversity(reranked, final_k)

        return diverse

    def _enhance_query(self, query: str) -> str:
        """Add context or expand query."""
        # HyDE: Generate hypothetical answer
        hypothetical = self.llm.invoke(
            f"Write a short paragraph that would answer: {query}"
        )
        return hypothetical

    def _initial_retrieval(self, query: str, k: int) -> list:
        """Fast retrieval with high recall."""
        embedding = embed(query)
        return self.vector_store.search(embedding, limit=k)

    def _pre_filter(self, candidates: list, query: str) -> list:
        """Remove obviously irrelevant results."""
        return [
            c for c in candidates
            if c.score > 0.3  # Minimum similarity
            and len(c.text) > 50  # Minimum content
        ]

    def _ensure_diversity(self, results: list, k: int) -> list:
        """Select diverse results using MMR."""
        return maximal_marginal_relevance(
            results,
            k=k,
            lambda_param=0.5  # Balance relevance/diversity
        )
```

### Pattern 2: Hypothetical Document Embeddings (HyDE)

```python
class HyDERetriever:
    """Generate hypothetical answer, then search for similar real docs."""

    def __init__(self, llm, embedder, vector_store):
        self.llm = llm
        self.embedder = embedder
        self.vector_store = vector_store

    def retrieve(self, query: str, k: int = 5) -> list:
        # Generate hypothetical document that would answer query
        hypothetical = self.llm.invoke(f"""
            Write a detailed paragraph that directly answers this question:
            {query}

            Write as if you're citing from a technical document.
        """)

        # Embed the hypothetical document
        hyde_embedding = self.embedder.embed(hypothetical)

        # Search for real documents similar to hypothetical
        results = self.vector_store.search(
            vector=hyde_embedding,
            limit=k
        )

        return results
```

### Pattern 3: Parent-Child Retrieval

```python
class ParentChildRetriever:
    """Retrieve small chunks, return parent documents."""

    def __init__(self, vector_store, document_store):
        self.vector_store = vector_store  # Stores child chunks
        self.document_store = document_store  # Stores parent docs

    def index(self, document: str, doc_id: str):
        """Index small chunks with parent reference."""

        # Create small chunks for retrieval
        chunks = chunk_text(document, chunk_size=200)

        for i, chunk in enumerate(chunks):
            chunk_id = f"{doc_id}_{i}"
            embedding = embed(chunk)

            self.vector_store.upsert({
                "id": chunk_id,
                "vector": embedding,
                "metadata": {
                    "parent_id": doc_id,
                    "chunk_index": i,
                    "text": chunk
                }
            })

        # Store full document
        self.document_store.set(doc_id, document)

    def retrieve(self, query: str, k: int = 3) -> list:
        """Retrieve chunks, return parent documents."""

        embedding = embed(query)

        # Find relevant chunks
        chunks = self.vector_store.search(embedding, limit=k * 3)

        # Get unique parent documents
        parent_ids = list(set(c.metadata["parent_id"] for c in chunks))

        # Retrieve full parent documents
        parents = []
        for pid in parent_ids[:k]:
            parent = self.document_store.get(pid)
            parents.append({
                "id": pid,
                "content": parent,
                "matched_chunks": [
                    c for c in chunks if c.metadata["parent_id"] == pid
                ]
            })

        return parents
```

### Pattern 4: Contextual Retrieval

```python
class ContextualRetriever:
    """Add document context to chunks before embedding."""

    def index_with_context(self, document: str, doc_title: str):
        """Add document context to each chunk."""

        # Generate document summary
        doc_summary = self.llm.invoke(
            f"Summarize this document in 2-3 sentences:\n\n{document}"
        )

        chunks = chunk_text(document, chunk_size=500)

        for chunk in chunks:
            # Prepend context to chunk
            contextualized = f"""
            Document: {doc_title}
            Summary: {doc_summary}

            Content: {chunk}
            """

            embedding = embed(contextualized)

            self.vector_store.upsert({
                "id": generate_id(),
                "vector": embedding,
                "metadata": {
                    "original_text": chunk,
                    "context": doc_summary,
                    "title": doc_title
                }
            })
```

### Pattern 5: Filtered Retrieval

```python
def filtered_search(
    query: str,
    embedding: list,
    vector_store,
    filters: dict,
    k: int = 10
) -> list:
    """Apply metadata filters before/during retrieval."""

    # Build filter expression
    filter_conditions = []

    if "category" in filters:
        filter_conditions.append({
            "field": "category",
            "match": {"value": filters["category"]}
        })

    if "date_range" in filters:
        filter_conditions.append({
            "field": "created_at",
            "range": {
                "gte": filters["date_range"]["start"],
                "lte": filters["date_range"]["end"]
            }
        })

    if "source" in filters:
        filter_conditions.append({
            "field": "source",
            "match": {"any": filters["source"]}
        })

    results = vector_store.search(
        vector=embedding,
        filter={"must": filter_conditions},
        limit=k
    )

    return results
```

## Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Vector-only search | Misses keyword matches | Add hybrid search |
| No reranking | First-stage errors persist | Use cross-encoder |
| Fixed k value | Too few or too many | Adaptive k or score threshold |
| Ignoring metadata | Can't filter by date/type | Rich metadata + filtering |
| Same query for all | Misses synonyms | Query expansion |

## Metrics to Track

```python
retrieval_metrics = {
    "quality": {
        "mrr": "Mean Reciprocal Rank",
        "ndcg": "Normalized Discounted Cumulative Gain",
        "recall@k": "Relevant docs in top k",
        "precision@k": "Relevant / Retrieved in top k"
    },
    "efficiency": {
        "latency_p50": "50th percentile latency",
        "latency_p99": "99th percentile latency",
        "tokens_retrieved": "Total tokens in context"
    },
    "coverage": {
        "empty_results_rate": "Queries with no results",
        "diversity_score": "Result diversity"
    }
}
```

## Tools & References

### Related Skills
- faion-vector-db-skill
- faion-embeddings-skill
- faion-llamaindex-skill

### Related Agents
- faion-rag-agent

### External Resources
- [Cohere Rerank](https://docs.cohere.com/docs/rerank)
- [LlamaIndex Retrievers](https://docs.llamaindex.ai/en/stable/module_guides/querying/retriever/)
- [HyDE Paper](https://arxiv.org/abs/2212.10496)
- [ColBERT](https://github.com/stanford-futuredata/ColBERT)

## Checklist

- [ ] Implemented hybrid search (vector + keyword)
- [ ] Added reranking stage
- [ ] Configured query expansion
- [ ] Set up metadata filtering
- [ ] Tuned k values for each stage
- [ ] Implemented diversity sampling
- [ ] Added score thresholds
- [ ] Set up retrieval metrics
- [ ] Tested with evaluation set
- [ ] Documented retrieval pipeline

---

*Methodology: M-RAG-004 | Category: RAG/Vector DB*
*Related: faion-rag-agent, faion-vector-db-skill, faion-embeddings-skill*
