# Embedding Applications

Benchmarking, vector database integration, and production usage patterns.

---

## Benchmarking

### MTEB Leaderboard

The Massive Text Embedding Benchmark (MTEB) is the standard for comparing embedding models.

| Model | Average Score | Retrieval | Classification | Clustering |
|-------|---------------|-----------|----------------|------------|
| bge-m3 | 68.1% | 66.8% | 75.2% | 48.3% |
| text-embedding-3-large | 64.6% | 63.4% | 75.8% | 46.1% |
| e5-mistral-7b-instruct | 66.6% | 60.5% | 78.4% | 51.2% |
| bge-large-en-v1.5 | 63.6% | 54.3% | 75.1% | 46.1% |
| text-embedding-3-small | 62.3% | 51.7% | 74.6% | 44.9% |

### Custom Benchmarking

```python
import numpy as np
from typing import Callable
from sklearn.metrics.pairwise import cosine_similarity

def benchmark_retrieval(
    queries: list[str],
    documents: list[str],
    relevance: dict[int, list[int]],  # query_idx -> [relevant_doc_idxs]
    embed_fn: Callable[[list[str]], np.ndarray],
    k: int = 10
) -> dict[str, float]:
    """
    Benchmark retrieval quality.

    Returns:
    - Recall@K
    - MRR (Mean Reciprocal Rank)
    - Precision@K
    """
    # Embed all
    query_embeddings = embed_fn(queries)
    doc_embeddings = embed_fn(documents)

    # Compute similarities
    similarities = cosine_similarity(query_embeddings, doc_embeddings)

    recalls, mrrs, precisions = [], [], []

    for q_idx, relevant_docs in relevance.items():
        # Get top-k results
        scores = similarities[q_idx]
        top_k_idxs = np.argsort(scores)[::-1][:k]

        # Recall@K
        hits = len(set(top_k_idxs) & set(relevant_docs))
        recalls.append(hits / len(relevant_docs))

        # MRR
        for rank, doc_idx in enumerate(top_k_idxs, 1):
            if doc_idx in relevant_docs:
                mrrs.append(1 / rank)
                break
        else:
            mrrs.append(0)

        # Precision@K
        precisions.append(hits / k)

    return {
        "recall@k": np.mean(recalls),
        "mrr": np.mean(mrrs),
        "precision@k": np.mean(precisions)
    }
```

### Speed Benchmarking

```python
import time
import statistics

def benchmark_speed(
    texts: list[str],
    embed_fn: Callable,
    iterations: int = 5
) -> dict[str, float]:
    """Benchmark embedding speed."""
    times = []

    for _ in range(iterations):
        start = time.perf_counter()
        embed_fn(texts)
        elapsed = time.perf_counter() - start
        times.append(elapsed)

    return {
        "mean_time": statistics.mean(times),
        "std_time": statistics.stdev(times) if len(times) > 1 else 0,
        "texts_per_second": len(texts) / statistics.mean(times),
        "ms_per_text": (statistics.mean(times) / len(texts)) * 1000
    }
```

---

## Integration with Vector Databases

### Storing Embeddings

```python
# Qdrant
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

client = QdrantClient("localhost", port=6333)
embeddings = get_embeddings_batch(texts)

points = [
    PointStruct(id=i, vector=emb, payload={"text": text})
    for i, (emb, text) in enumerate(zip(embeddings, texts))
]
client.upsert("my_collection", points)

# pgvector
import psycopg2

conn = psycopg2.connect("postgresql://...")
cur = conn.cursor()

for text, embedding in zip(texts, embeddings):
    cur.execute(
        "INSERT INTO documents (content, embedding) VALUES (%s, %s)",
        (text, embedding)
    )
conn.commit()
```

### Searching

```python
# Qdrant
query_embedding = get_embedding(query)
results = client.search(
    collection_name="my_collection",
    query_vector=query_embedding,
    limit=10
)

# pgvector
cur.execute("""
    SELECT content, 1 - (embedding <=> %s) as similarity
    FROM documents
    ORDER BY embedding <=> %s
    LIMIT 10
""", (query_embedding, query_embedding))
```

---

## References

- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)
- [Sentence Transformers](https://www.sbert.net/)
- [BGE-M3 Paper](https://arxiv.org/abs/2402.03216)
- [Matryoshka Representation Learning](https://arxiv.org/abs/2205.13147)
- [Chunking Strategies Guide](https://www.pinecone.io/learn/chunking-strategies/)

## Sources

- [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)
- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)
- [Sentence Transformers](https://www.sbert.net/)
- [BGE-M3 Paper](https://arxiv.org/abs/2402.03216)
- [Matryoshka Embeddings](https://arxiv.org/abs/2205.13147)
