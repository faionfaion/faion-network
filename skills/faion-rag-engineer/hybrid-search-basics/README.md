---
id: hybrid-search-basics
name: "Hybrid Search Basics"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Hybrid Search Basics

## Overview

Hybrid search combines semantic (vector) search with lexical (keyword) search to leverage the strengths of both approaches. Semantic search excels at understanding meaning, while lexical search captures exact matches and rare terms. Together, they provide more robust retrieval.

## When to Use

- Technical documentation with specific terminology
- Legal or medical domains with exact phrase requirements
- When queries mix conceptual and specific terms
- Improving recall over pure vector search
- When users search using exact product names or codes

## Key Concepts

### Search Types Comparison

| Aspect | Semantic Search | Lexical Search | Hybrid |
|--------|-----------------|----------------|--------|
| Meaning | Understands context | Literal matching | Both |
| Rare terms | May miss | Excels | Captures |
| Synonyms | Handles well | Misses | Handles |
| Speed | Slower | Fast | Balanced |
| Typos | Tolerant | Sensitive | Moderate |

### Fusion Strategies

```
┌─────────────────┐     ┌─────────────────┐
│  Vector Search  │     │ Keyword Search  │
│  (Semantic)     │     │ (BM25/TF-IDF)   │
└────────┬────────┘     └────────┬────────┘
         │                       │
         └───────────┬───────────┘
                     │
              ┌──────▼──────┐
              │   Fusion    │
              │  Strategy   │
              └──────┬──────┘
                     │
              ┌──────▼──────┐
              │   Ranked    │
              │   Results   │
              └─────────────┘
```

## Basic Implementation

### Simple Hybrid Search

```python
from typing import List, Dict, Tuple
import numpy as np
from rank_bm25 import BM25Okapi
import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt', quiet=True)

class HybridSearch:
    """Combine vector and BM25 search."""

    def __init__(
        self,
        documents: List[Dict],
        embedding_func: callable,
        alpha: float = 0.5  # Weight for semantic (1-alpha for keyword)
    ):
        self.documents = documents
        self.embedding_func = embedding_func
        self.alpha = alpha

        # Build indices
        self._build_bm25_index()
        self._build_vector_index()

    def _build_bm25_index(self):
        """Build BM25 keyword index."""
        tokenized_docs = [
            word_tokenize(doc["content"].lower())
            for doc in self.documents
        ]
        self.bm25 = BM25Okapi(tokenized_docs)

    def _build_vector_index(self):
        """Build vector index."""
        self.embeddings = np.array([
            self.embedding_func(doc["content"])
            for doc in self.documents
        ])
        # Normalize for cosine similarity
        norms = np.linalg.norm(self.embeddings, axis=1, keepdims=True)
        self.embeddings = self.embeddings / norms

    def search(
        self,
        query: str,
        top_k: int = 10
    ) -> List[Tuple[Dict, float]]:
        """Execute hybrid search."""
        # Semantic search
        query_embedding = self.embedding_func(query)
        query_embedding = query_embedding / np.linalg.norm(query_embedding)
        semantic_scores = np.dot(self.embeddings, query_embedding)

        # BM25 search
        tokenized_query = word_tokenize(query.lower())
        bm25_scores = self.bm25.get_scores(tokenized_query)

        # Normalize scores to [0, 1]
        semantic_scores = self._normalize(semantic_scores)
        bm25_scores = self._normalize(bm25_scores)

        # Combine scores
        combined_scores = (
            self.alpha * semantic_scores +
            (1 - self.alpha) * bm25_scores
        )

        # Get top-k
        top_indices = np.argsort(combined_scores)[::-1][:top_k]

        return [
            (self.documents[i], combined_scores[i])
            for i in top_indices
        ]

    def _normalize(self, scores: np.ndarray) -> np.ndarray:
        """Min-max normalization."""
        min_score = scores.min()
        max_score = scores.max()
        if max_score == min_score:
            return np.zeros_like(scores)
        return (scores - min_score) / (max_score - min_score)
```

## Fusion Methods

### Reciprocal Rank Fusion (RRF)

```python
from collections import defaultdict

def reciprocal_rank_fusion(
    rankings: List[List[str]],  # List of ranked document ID lists
    k: int = 60  # RRF constant
) -> List[Tuple[str, float]]:
    """
    Combine multiple rankings using Reciprocal Rank Fusion.
    RRF is more robust than simple score averaging.
    """
    rrf_scores = defaultdict(float)

    for ranking in rankings:
        for rank, doc_id in enumerate(ranking):
            rrf_scores[doc_id] += 1.0 / (k + rank + 1)

    # Sort by RRF score
    sorted_results = sorted(
        rrf_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return sorted_results

# Usage example
vector_ranking = ["doc1", "doc3", "doc2", "doc5", "doc4"]
bm25_ranking = ["doc2", "doc1", "doc4", "doc3", "doc6"]

fused = reciprocal_rank_fusion([vector_ranking, bm25_ranking])
# Result: [('doc1', 0.032), ('doc2', 0.032), ('doc3', 0.031), ...]
```

### Dynamic Alpha Selection

```python
def determine_alpha(query: str) -> float:
    """
    Dynamically select alpha based on query characteristics.
    """
    # Check for exact match indicators
    has_quotes = '"' in query
    has_codes = any(char.isdigit() for char in query)
    is_short = len(query.split()) <= 3

    # More specific queries → more keyword weight
    if has_quotes:
        return 0.3  # Favor keyword search
    elif has_codes:
        return 0.4
    elif is_short:
        return 0.5  # Balanced
    else:
        return 0.7  # Favor semantic for longer queries

def intelligent_hybrid_search(
    search_engine,
    query: str,
    top_k: int = 10
) -> list:
    """Hybrid search with dynamic alpha."""
    alpha = determine_alpha(query)
    return search_engine.search(query, alpha=alpha, top_k=top_k)
```

## Best Practices

1. **Alpha Tuning**
   - Start with 0.5 and tune based on query types
   - Use higher alpha for conceptual queries
   - Use lower alpha for specific/technical queries

2. **Fusion Method Selection**
   - RRF is generally more robust
   - Linear fusion is faster
   - Test both on your data

3. **Index Optimization**
   - Use appropriate BM25 parameters for your domain
   - Consider stop words for keyword search
   - Normalize vectors for cosine similarity

4. **Query Analysis**
   - Detect query type dynamically
   - Handle edge cases (empty queries, very long queries)
   - Log and analyze search patterns

5. **Evaluation**
   - Compare hybrid vs. pure approaches
   - Test on diverse query sets
   - Monitor production performance

## Common Pitfalls

1. **Score Scale Mismatch** - Not normalizing scores before fusion
2. **Wrong Alpha** - Using same alpha for all query types
3. **BM25 Without Preprocessing** - Not handling stop words, case
4. **Ignoring Rare Terms** - Semantic search missing exact matches
5. **Over-relying on One Method** - Not testing both components separately
6. **No Query Analysis** - Static approach for dynamic queries

## Sources

- [Reciprocal Rank Fusion Paper](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)
- [BM25 Algorithm Explained](https://en.wikipedia.org/wiki/Okapi_BM25)
- [Hybrid Search with Qdrant](https://qdrant.tech/articles/hybrid-search/)
- [LangChain Ensemble Retriever](https://python.langchain.com/docs/modules/data_connection/retrievers/ensemble/)
