# Embedding Basics

Text embeddings are numerical vector representations of text that capture semantic meaning.

---

## Quick Reference

### Model Comparison

| Model | Provider | Dimensions | Max Tokens | Cost/1M tokens | Quality | Speed |
|-------|----------|------------|------------|----------------|---------|-------|
| **text-embedding-3-large** | OpenAI | 3072 (256-3072) | 8191 | $0.13 | Best | Fast |
| **text-embedding-3-small** | OpenAI | 1536 (256-1536) | 8191 | $0.02 | Good | Fast |
| **text-embedding-ada-002** | OpenAI | 1536 | 8191 | $0.10 | Good | Fast |
| **mistral-embed** | Mistral | 1024 | 8192 | $0.10 | Good | Fast |
| **embed-english-v3.0** | Cohere | 1024 | 512 | $0.10 | Very Good | Fast |
| **embed-multilingual-v3.0** | Cohere | 1024 | 512 | $0.10 | Very Good | Fast |
| **bge-large-en-v1.5** | Local | 1024 | 512 | Free | Very Good | Medium |
| **bge-m3** | Local | 1024 | 8192 | Free | Excellent | Slow |
| **all-MiniLM-L6-v2** | Local | 384 | 256 | Free | Adequate | Very Fast |
| **e5-large-v2** | Local | 1024 | 512 | Free | Very Good | Medium |
| **gte-large** | Local | 1024 | 512 | Free | Very Good | Medium |
| **nomic-embed-text-v1.5** | Local | 768 | 8192 | Free | Good | Fast |

### When to Use Which

| Use Case | Recommended Model | Why |
|----------|-------------------|-----|
| **Production RAG** | text-embedding-3-large | Best quality, scalable |
| **Cost-sensitive** | text-embedding-3-small or local BGE | Good quality, low cost |
| **Multilingual** | embed-multilingual-v3.0 or bge-m3 | 100+ languages |
| **Long documents** | bge-m3 or nomic-embed | 8K token context |
| **Air-gapped/Private** | sentence-transformers (local) | No API calls |
| **Real-time search** | all-MiniLM-L6-v2 | Fast inference |
| **Semantic similarity** | e5-large-v2 | Trained for similarity |

---

## Chunking Strategies

### Why Chunking Matters

Embedding models have token limits. Long documents must be split into chunks.

### Fixed-Size Chunks

```python
def chunk_fixed_size(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50
) -> list[str]:
    """Split text into fixed-size chunks with overlap."""
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start = end - overlap

    return chunks
```

### Token-Based Chunks (Recommended)

```python
import tiktoken

def chunk_by_tokens(
    text: str,
    max_tokens: int = 500,
    overlap_tokens: int = 50,
    model: str = "text-embedding-3-large"
) -> list[str]:
    """Split text by token count (more accurate)."""
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    chunks = []
    start = 0

    while start < len(tokens):
        end = min(start + max_tokens, len(tokens))
        chunk_tokens = tokens[start:end]
        chunk_text = encoding.decode(chunk_tokens)
        chunks.append(chunk_text)
        start = end - overlap_tokens

    return chunks
```

### Semantic Chunking

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_semantic(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> list[str]:
    """Split at natural boundaries (paragraphs, sentences)."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    return splitter.split_text(text)
```

### Sentence-Based Chunks

```python
import nltk
nltk.download('punkt')

def chunk_by_sentences(
    text: str,
    sentences_per_chunk: int = 5,
    overlap_sentences: int = 1
) -> list[str]:
    """Split by sentences for better semantic coherence."""
    sentences = nltk.sent_tokenize(text)
    chunks = []
    start = 0

    while start < len(sentences):
        end = start + sentences_per_chunk
        chunk = " ".join(sentences[start:end])
        chunks.append(chunk)
        start = end - overlap_sentences

    return chunks
```

### Optimal Chunk Sizes

| Use Case | Chunk Size | Overlap | Rationale |
|----------|------------|---------|-----------|
| **Q&A RAG** | 256-512 tokens | 20% | Focused answers |
| **Document summary** | 1000-2000 tokens | 10% | More context |
| **Code search** | 100-200 tokens | 50% | Preserve functions |
| **Legal/Medical** | 500-1000 tokens | 25% | Complete clauses |

---

## Caching Strategies

### In-Memory Cache

```python
import hashlib
from functools import lru_cache
from typing import Tuple

def text_hash(text: str) -> str:
    """Create consistent hash for text."""
    return hashlib.sha256(text.encode()).hexdigest()[:16]

@lru_cache(maxsize=10000)
def get_embedding_cached(text_hash: str, text: str, model: str) -> Tuple[float, ...]:
    """Cache embeddings in memory."""
    embedding = get_embedding(text, model)
    return tuple(embedding)  # Tuples are hashable
```

### File-Based Cache

```python
import json
import hashlib
from pathlib import Path

class EmbeddingCache:
    def __init__(self, cache_dir: str = ".embedding_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def _get_key(self, text: str, model: str) -> str:
        content = f"{model}:{text}"
        return hashlib.sha256(content.encode()).hexdigest()

    def get(self, text: str, model: str) -> list[float] | None:
        key = self._get_key(text, model)
        cache_file = self.cache_dir / f"{key}.json"

        if cache_file.exists():
            return json.loads(cache_file.read_text())
        return None

    def set(self, text: str, model: str, embedding: list[float]):
        key = self._get_key(text, model)
        cache_file = self.cache_dir / f"{key}.json"
        cache_file.write_text(json.dumps(embedding))

    def get_or_compute(
        self,
        text: str,
        model: str,
        compute_fn
    ) -> list[float]:
        cached = self.get(text, model)
        if cached:
            return cached

        embedding = compute_fn(text, model)
        self.set(text, model, embedding)
        return embedding
```

### Redis Cache (Production)

```python
import redis
import json
import hashlib

class RedisEmbeddingCache:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.client = redis.from_url(redis_url)
        self.ttl = 86400 * 30  # 30 days

    def _get_key(self, text: str, model: str) -> str:
        content = f"{model}:{text}"
        hash_val = hashlib.sha256(content.encode()).hexdigest()
        return f"emb:{hash_val}"

    def get(self, text: str, model: str) -> list[float] | None:
        key = self._get_key(text, model)
        data = self.client.get(key)
        return json.loads(data) if data else None

    def set(self, text: str, model: str, embedding: list[float]):
        key = self._get_key(text, model)
        self.client.setex(key, self.ttl, json.dumps(embedding))

    def get_batch(
        self,
        texts: list[str],
        model: str
    ) -> dict[str, list[float] | None]:
        """Get multiple embeddings from cache."""
        pipe = self.client.pipeline()
        keys = [self._get_key(t, model) for t in texts]

        for key in keys:
            pipe.get(key)

        results = pipe.execute()
        return {
            text: json.loads(data) if data else None
            for text, data in zip(texts, results)
        }
```

---

## Cost Optimization

### Cost Comparison

| Model | Cost/1M tokens | 1M docs (500 tokens) | Monthly (10M docs) |
|-------|----------------|----------------------|-------------------|
| text-embedding-3-large | $0.13 | $0.065 | $650 |
| text-embedding-3-small | $0.02 | $0.010 | $100 |
| mistral-embed | $0.10 | $0.050 | $500 |
| Local (GPU) | ~$0.001 | ~$0.0005 | ~$5 (compute) |
| Local (CPU) | ~$0.005 | ~$0.0025 | ~$25 (compute) |

### Optimization Strategies

#### 1. Use Dimension Reduction

```python
# Instead of 3072 dimensions ($0.13/1M)
# Use 1024 dimensions with minimal quality loss
embedding = get_embedding_reduced(text, dimensions=1024)
# Saves 66% storage, similar retrieval quality
```

#### 2. Batch Requests

```python
# Bad: 1000 API calls
for text in texts:
    get_embedding(text)  # 1000 requests

# Good: 1 API call
get_embeddings_batch(texts)  # 1 request for up to 2048 texts
```

#### 3. Cache Aggressively

```python
# Cache hit rate of 80% = 80% cost reduction
cache = RedisEmbeddingCache()
embedding = cache.get_or_compute(text, model, get_embedding)
```

#### 4. Use Smaller Models for Filtering

```python
# Two-stage retrieval:
# 1. Fast filter with small model
quick_results = search_with_model(query, "all-MiniLM-L6-v2", top_k=100)

# 2. Rerank with large model
final_results = rerank_with_model(query, quick_results, "text-embedding-3-large", top_k=10)
```

#### 5. Deduplicate Before Embedding

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def deduplicate_texts(texts: list[str], threshold: float = 0.95) -> list[str]:
    """Remove near-duplicate texts before embedding."""
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)

    unique_texts = []
    for i, text in enumerate(texts):
        if not unique_texts:
            unique_texts.append(text)
            continue

        # Compare with existing
        current_vec = tfidf_matrix[i]
        existing_vecs = vectorizer.transform(unique_texts)
        similarities = cosine_similarity(current_vec, existing_vecs)[0]

        if max(similarities) < threshold:
            unique_texts.append(text)

    return unique_texts
```

---

## References

- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)
- [Sentence Transformers](https://www.sbert.net/)
- [Chunking Strategies Guide](https://www.pinecone.io/learn/chunking-strategies/)

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Analyze and assess | sonnet | Evaluation and planning |
| Execute implementation | haiku | Apply established patterns |
| Review and validate | sonnet | Quality assurance |
| Strategic decision | opus | Novel scenarios |
| Optimize and refine | haiku | Performance tuning |
| Document approach | haiku | Create documentation |

## Sources

- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)
- [Sentence Transformers](https://www.sbert.net/)
- [Voyage AI Embeddings](https://docs.voyageai.com/docs/embeddings)
- [Cohere Embed v3](https://docs.cohere.com/docs/cohere-embed)
