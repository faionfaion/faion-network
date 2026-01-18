# M-RAG-002: Embedding Selection

## Overview

Embedding models convert text into dense vector representations for semantic similarity search. Model selection impacts retrieval quality, speed, and cost. Considerations include dimensionality, multilingual support, and task-specific performance.

**When to use:** Choosing embedding models for RAG systems, semantic search, or clustering applications.

## Core Concepts

### 1. Embedding Model Comparison (2025)

| Model | Dimensions | Context | MTEB Score | Speed | Cost |
|-------|------------|---------|------------|-------|------|
| **OpenAI text-embedding-3-large** | 3072 | 8191 | 64.6 | Fast | $0.13/1M |
| **OpenAI text-embedding-3-small** | 1536 | 8191 | 62.3 | Fastest | $0.02/1M |
| **Cohere embed-v3** | 1024 | 512 | 64.5 | Fast | $0.10/1M |
| **Voyage voyage-3** | 1024 | 32K | 67.1 | Medium | $0.06/1M |
| **BGE-M3** | 1024 | 8192 | 66.3 | Medium | Free |
| **E5-mistral-7b** | 4096 | 32K | 66.6 | Slow | Free |
| **GTE-Qwen2** | 1536 | 8192 | 67.2 | Medium | Free |
| **nomic-embed-text** | 768 | 8192 | 62.4 | Fast | Free |

### 2. Key Metrics

| Metric | Description | Why It Matters |
|--------|-------------|----------------|
| **MTEB Score** | Massive Text Embedding Benchmark | Overall quality |
| **Dimensions** | Vector size | Storage, compute |
| **Context Length** | Max tokens per embedding | Document handling |
| **Latency** | Time to embed | User experience |
| **Cost** | Price per million tokens | Scale economics |
| **Multilingual** | Language support | Global use |

### 3. Embedding Types

| Type | Use Case | Example Models |
|------|----------|----------------|
| **Dense** | Semantic similarity | OpenAI, Cohere |
| **Sparse** | Keyword matching | SPLADE, BM25 |
| **Hybrid** | Best of both | BGE-M3, Cohere |
| **Late interaction** | Fine-grained | ColBERT |
| **Multimodal** | Text + images | CLIP, Jina CLIP |

## Best Practices

### 1. Match Model to Task

```python
def select_embedding_model(task: str, constraints: dict) -> str:
    """Select appropriate embedding model based on task."""

    recommendations = {
        "semantic_search": {
            "budget": "text-embedding-3-small",
            "quality": "voyage-3",
            "free": "bge-m3"
        },
        "rag_retrieval": {
            "budget": "text-embedding-3-small",
            "quality": "text-embedding-3-large",
            "free": "gte-qwen2"
        },
        "multilingual": {
            "budget": "text-embedding-3-small",
            "quality": "cohere-embed-v3",
            "free": "bge-m3"
        },
        "code_search": {
            "budget": "text-embedding-3-small",
            "quality": "voyage-code-2",
            "free": "codebert"
        },
        "long_documents": {
            "budget": "voyage-3",
            "quality": "voyage-3",
            "free": "e5-mistral-7b"
        }
    }

    priority = "quality" if constraints.get("quality_first") else "budget"
    if constraints.get("free_only"):
        priority = "free"

    return recommendations.get(task, recommendations["semantic_search"])[priority]
```

### 2. Optimize Dimensions

```python
from openai import OpenAI

client = OpenAI()

def get_embedding(text: str, dimensions: int = 1536) -> list:
    """Get embedding with dimension reduction."""

    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=text,
        dimensions=dimensions  # Reduce from 3072 to desired
    )

    return response.data[0].embedding

# Trade-offs
dimension_options = {
    256: "80% of quality, 12x compression",
    512: "90% of quality, 6x compression",
    1024: "95% of quality, 3x compression",
    1536: "98% of quality, 2x compression",
    3072: "100% quality, no compression"
}
```

### 3. Batch for Efficiency

```python
import asyncio
from typing import List

async def batch_embed(
    texts: List[str],
    batch_size: int = 100,
    model: str = "text-embedding-3-small"
) -> List[List[float]]:
    """Embed texts in batches for efficiency."""

    embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]

        response = await client.embeddings.create(
            model=model,
            input=batch
        )

        batch_embeddings = [item.embedding for item in response.data]
        embeddings.extend(batch_embeddings)

    return embeddings

# Cost calculation
def estimate_cost(texts: List[str], model: str) -> float:
    pricing = {
        "text-embedding-3-small": 0.02,
        "text-embedding-3-large": 0.13
    }

    total_tokens = sum(count_tokens(t) for t in texts)
    cost = (total_tokens / 1_000_000) * pricing[model]
    return cost
```

## Common Patterns

### Pattern 1: OpenAI Embeddings

```python
from openai import OpenAI

client = OpenAI()

def embed_with_openai(texts: list[str], model: str = "text-embedding-3-small"):
    """Generate embeddings using OpenAI."""

    response = client.embeddings.create(
        model=model,
        input=texts,
        encoding_format="float"  # or "base64" for smaller payloads
    )

    return [item.embedding for item in response.data]

# Usage
texts = ["Hello world", "Semantic search example"]
embeddings = embed_with_openai(texts)
```

### Pattern 2: Local Embeddings with Sentence Transformers

```python
from sentence_transformers import SentenceTransformer

# Load model (downloads on first use)
model = SentenceTransformer("BAAI/bge-m3")

def embed_local(texts: list[str], normalize: bool = True) -> list:
    """Generate embeddings locally."""

    embeddings = model.encode(
        texts,
        normalize_embeddings=normalize,
        show_progress_bar=True,
        batch_size=32
    )

    return embeddings.tolist()

# For GPU acceleration
model = SentenceTransformer("BAAI/bge-m3", device="cuda")
```

### Pattern 3: Hybrid Embeddings

```python
from FlagEmbedding import BGEM3FlagModel

class HybridEmbedder:
    """Generate dense and sparse embeddings."""

    def __init__(self):
        self.model = BGEM3FlagModel(
            "BAAI/bge-m3",
            use_fp16=True
        )

    def embed(self, texts: list[str]) -> dict:
        """Return both dense and sparse representations."""

        output = self.model.encode(
            texts,
            return_dense=True,
            return_sparse=True,
            return_colbert_vecs=False
        )

        return {
            "dense": output["dense_vecs"],
            "sparse": output["lexical_weights"]  # Dict of token -> weight
        }

    def search(self, query: str, corpus_embeddings: dict) -> list:
        """Hybrid search combining dense and sparse."""

        query_emb = self.embed([query])

        # Dense similarity
        dense_scores = cosine_similarity(
            query_emb["dense"],
            corpus_embeddings["dense"]
        )

        # Sparse similarity (BM25-like)
        sparse_scores = sparse_dot_product(
            query_emb["sparse"][0],
            corpus_embeddings["sparse"]
        )

        # Combine scores (weighted average)
        combined = 0.7 * dense_scores + 0.3 * sparse_scores

        return combined
```

### Pattern 4: Embedding Cache

```python
import hashlib
import redis
import pickle

class EmbeddingCache:
    def __init__(self, redis_url: str, model: str):
        self.redis = redis.from_url(redis_url)
        self.model = model
        self.ttl = 86400 * 7  # 7 days

    def _get_key(self, text: str) -> str:
        text_hash = hashlib.sha256(text.encode()).hexdigest()[:16]
        return f"emb:{self.model}:{text_hash}"

    def get(self, text: str) -> list | None:
        key = self._get_key(text)
        cached = self.redis.get(key)
        if cached:
            return pickle.loads(cached)
        return None

    def set(self, text: str, embedding: list):
        key = self._get_key(text)
        self.redis.setex(key, self.ttl, pickle.dumps(embedding))

    def get_or_embed(self, texts: list[str], embed_func) -> list:
        """Get cached or compute new embeddings."""

        results = [None] * len(texts)
        to_embed = []
        to_embed_indices = []

        # Check cache
        for i, text in enumerate(texts):
            cached = self.get(text)
            if cached:
                results[i] = cached
            else:
                to_embed.append(text)
                to_embed_indices.append(i)

        # Compute missing
        if to_embed:
            new_embeddings = embed_func(to_embed)

            for i, (text, emb) in enumerate(zip(to_embed, new_embeddings)):
                results[to_embed_indices[i]] = emb
                self.set(text, emb)

        return results
```

### Pattern 5: Multimodal Embeddings

```python
from transformers import AutoProcessor, AutoModel
import torch

class MultimodalEmbedder:
    def __init__(self, model_name: str = "jinaai/jina-clip-v2"):
        self.processor = AutoProcessor.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def embed_text(self, texts: list[str]) -> torch.Tensor:
        """Embed text into shared embedding space."""

        inputs = self.processor(
            text=texts,
            return_tensors="pt",
            padding=True
        )

        with torch.no_grad():
            embeddings = self.model.get_text_features(**inputs)

        return embeddings

    def embed_image(self, images: list) -> torch.Tensor:
        """Embed images into shared embedding space."""

        inputs = self.processor(
            images=images,
            return_tensors="pt"
        )

        with torch.no_grad():
            embeddings = self.model.get_image_features(**inputs)

        return embeddings

    def cross_modal_search(self, query_text: str, image_embeddings: torch.Tensor):
        """Search images using text query."""

        text_emb = self.embed_text([query_text])
        similarities = torch.cosine_similarity(text_emb, image_embeddings)
        return similarities
```

## Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| One model for all | Suboptimal performance | Task-specific models |
| Ignoring dimensions | Wasted storage | Use dimension reduction |
| No caching | Redundant API calls | Cache embeddings |
| Sync batch processing | Slow for large sets | Async/parallel |
| Mismatched embeddings | Can't compare | Same model for query/docs |

## Evaluation Framework

```python
def evaluate_embedding_model(model, test_set: list[dict]) -> dict:
    """Evaluate embedding model on retrieval task."""

    metrics = {
        "mrr": [],  # Mean Reciprocal Rank
        "recall@5": [],
        "recall@10": [],
        "latency_ms": []
    }

    for case in test_set:
        query = case["query"]
        relevant_ids = set(case["relevant_doc_ids"])

        start = time.time()
        query_emb = model.embed([query])[0]
        latency = (time.time() - start) * 1000

        # Retrieve top-k
        results = vector_store.search(query_emb, k=10)
        retrieved_ids = [r.id for r in results]

        # Calculate metrics
        metrics["latency_ms"].append(latency)
        metrics["recall@5"].append(
            len(set(retrieved_ids[:5]) & relevant_ids) / len(relevant_ids)
        )
        metrics["recall@10"].append(
            len(set(retrieved_ids[:10]) & relevant_ids) / len(relevant_ids)
        )

        for rank, doc_id in enumerate(retrieved_ids, 1):
            if doc_id in relevant_ids:
                metrics["mrr"].append(1 / rank)
                break
        else:
            metrics["mrr"].append(0)

    return {k: sum(v) / len(v) for k, v in metrics.items()}
```

## Tools & References

### Related Skills
- faion-embeddings-skill
- faion-vector-db-skill
- faion-openai-api-skill

### Related Agents
- faion-embedding-agent
- faion-rag-agent

### External Resources
- [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)
- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)
- [Sentence Transformers](https://www.sbert.net/)
- [BGE-M3](https://huggingface.co/BAAI/bge-m3)

## Checklist

- [ ] Identified use case requirements
- [ ] Evaluated model options on MTEB
- [ ] Tested with representative data
- [ ] Optimized dimensions for storage
- [ ] Implemented batching
- [ ] Set up caching
- [ ] Measured latency and quality
- [ ] Documented model choice
- [ ] Planned for model updates

---

*Methodology: M-RAG-002 | Category: RAG/Vector DB*
*Related: faion-embedding-agent, faion-embeddings-skill, faion-vector-db-skill*
