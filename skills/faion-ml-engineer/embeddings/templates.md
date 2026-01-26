# Embedding Pipeline Templates

Production-ready templates for embedding generation, batch processing, caching, and complete RAG pipelines.

---

## Table of Contents

1. [Provider Templates](#provider-templates)
2. [Batch Processing Templates](#batch-processing-templates)
3. [Caching Templates](#caching-templates)
4. [Complete Pipeline Templates](#complete-pipeline-templates)
5. [Configuration Templates](#configuration-templates)
6. [Testing Templates](#testing-templates)

---

## Provider Templates

### OpenAI Embedding Service

```python
"""OpenAI embedding service with retry, batching, and dimension reduction."""

from dataclasses import dataclass
from typing import Callable
import time
import random

from openai import OpenAI, RateLimitError, APIError


@dataclass
class OpenAIEmbeddingConfig:
    """Configuration for OpenAI embeddings."""
    model: str = "text-embedding-3-large"
    dimensions: int | None = None  # None = full dimensions
    batch_size: int = 2048
    max_retries: int = 5
    base_delay: float = 1.0


class OpenAIEmbeddingService:
    """OpenAI embedding service with production features."""

    def __init__(self, config: OpenAIEmbeddingConfig | None = None):
        self.config = config or OpenAIEmbeddingConfig()
        self.client = OpenAI()

    def embed_single(self, text: str) -> list[float]:
        """Embed single text with retry logic."""
        return self._embed_with_retry([text])[0]

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple texts efficiently."""
        all_embeddings = []

        for i in range(0, len(texts), self.config.batch_size):
            batch = texts[i:i + self.config.batch_size]
            embeddings = self._embed_with_retry(batch)
            all_embeddings.extend(embeddings)

        return all_embeddings

    def _embed_with_retry(self, texts: list[str]) -> list[list[float]]:
        """Embed with exponential backoff retry."""
        for attempt in range(self.config.max_retries):
            try:
                kwargs = {
                    "input": texts,
                    "model": self.config.model
                }
                if self.config.dimensions:
                    kwargs["dimensions"] = self.config.dimensions

                response = self.client.embeddings.create(**kwargs)
                sorted_data = sorted(response.data, key=lambda x: x.index)
                return [e.embedding for e in sorted_data]

            except RateLimitError:
                delay = self._calculate_delay(attempt)
                print(f"Rate limited. Waiting {delay:.1f}s...")
                time.sleep(delay)

            except APIError as e:
                if attempt == self.config.max_retries - 1:
                    raise
                delay = self.config.base_delay + random.random()
                print(f"API error: {e}. Retrying in {delay:.1f}s...")
                time.sleep(delay)

        raise Exception("Max retries exceeded")

    def _calculate_delay(self, attempt: int) -> float:
        """Calculate exponential backoff delay."""
        return (2 ** attempt) * self.config.base_delay + random.random()


# Usage
if __name__ == "__main__":
    config = OpenAIEmbeddingConfig(
        model="text-embedding-3-large",
        dimensions=1024,  # Reduced dimensions
        batch_size=100
    )
    service = OpenAIEmbeddingService(config)

    # Single embedding
    emb = service.embed_single("Hello world")
    print(f"Dimensions: {len(emb)}")

    # Batch embedding
    texts = [f"Document {i}" for i in range(500)]
    embeddings = service.embed_batch(texts)
    print(f"Embedded {len(embeddings)} documents")
```

### Voyage AI Embedding Service

```python
"""Voyage AI embedding service with asymmetric search and quantization."""

from dataclasses import dataclass
from typing import Literal
import voyageai


@dataclass
class VoyageEmbeddingConfig:
    """Configuration for Voyage AI embeddings."""
    model: str = "voyage-3.5"
    output_dimension: int = 1024
    output_dtype: Literal["float", "int8", "binary"] = "float"
    batch_size: int = 128


class VoyageEmbeddingService:
    """Voyage AI embedding service with asymmetric search."""

    def __init__(self, config: VoyageEmbeddingConfig | None = None):
        self.config = config or VoyageEmbeddingConfig()
        self.client = voyageai.Client()

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Embed documents for indexing."""
        return self._embed_batch(texts, input_type="document")

    def embed_queries(self, queries: list[str]) -> list[list[float]]:
        """Embed queries for search."""
        return self._embed_batch(queries, input_type="query")

    def embed_query(self, query: str) -> list[float]:
        """Embed single query."""
        return self.embed_queries([query])[0]

    def _embed_batch(
        self,
        texts: list[str],
        input_type: str
    ) -> list[list[float]]:
        """Embed texts in batches."""
        all_embeddings = []

        for i in range(0, len(texts), self.config.batch_size):
            batch = texts[i:i + self.config.batch_size]
            result = self.client.embed(
                texts=batch,
                model=self.config.model,
                input_type=input_type,
                output_dimension=self.config.output_dimension,
                output_dtype=self.config.output_dtype
            )
            all_embeddings.extend(result.embeddings)

        return all_embeddings


# Usage
if __name__ == "__main__":
    config = VoyageEmbeddingConfig(
        model="voyage-3.5",
        output_dimension=512,  # Smaller for cost savings
        output_dtype="int8"    # Quantized
    )
    service = VoyageEmbeddingService(config)

    # Asymmetric search
    docs = ["Python tutorial", "Java guide"]
    doc_embs = service.embed_documents(docs)

    query_emb = service.embed_query("programming language")
    print(f"Document dims: {len(doc_embs[0])}, Query dims: {len(query_emb)}")
```

### Cohere Embedding Service

```python
"""Cohere embedding service with multimodal support."""

from dataclasses import dataclass
from typing import Literal
import base64
from pathlib import Path
import cohere


@dataclass
class CohereEmbeddingConfig:
    """Configuration for Cohere embeddings."""
    model: str = "embed-v4"
    dimensions: int = 1024
    truncate: Literal["START", "END", "NONE"] = "END"


class CohereEmbeddingService:
    """Cohere embedding service with multimodal and input types."""

    def __init__(self, config: CohereEmbeddingConfig | None = None):
        self.config = config or CohereEmbeddingConfig()
        self.client = cohere.Client()

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Embed documents for indexing."""
        return self._embed_texts(texts, input_type="search_document")

    def embed_queries(self, queries: list[str]) -> list[list[float]]:
        """Embed queries for search."""
        return self._embed_texts(queries, input_type="search_query")

    def embed_for_classification(self, texts: list[str]) -> list[list[float]]:
        """Embed texts for classification tasks."""
        return self._embed_texts(texts, input_type="classification")

    def embed_for_clustering(self, texts: list[str]) -> list[list[float]]:
        """Embed texts for clustering tasks."""
        return self._embed_texts(texts, input_type="clustering")

    def embed_images(self, image_paths: list[str]) -> list[list[float]]:
        """Embed images (embed-v4 only)."""
        images_b64 = []
        for path in image_paths:
            image_bytes = Path(path).read_bytes()
            images_b64.append(base64.standard_b64encode(image_bytes).decode("utf-8"))

        response = self.client.embed(
            model=self.config.model,
            input_type="image",
            images=images_b64,
            output_dimension=self.config.dimensions
        )
        return response.embeddings

    def _embed_texts(
        self,
        texts: list[str],
        input_type: str
    ) -> list[list[float]]:
        """Embed texts with specified input type."""
        response = self.client.embed(
            texts=texts,
            model=self.config.model,
            input_type=input_type,
            truncate=self.config.truncate,
            output_dimension=self.config.dimensions
        )
        return response.embeddings


# Usage
if __name__ == "__main__":
    service = CohereEmbeddingService()

    # Text embeddings
    docs = ["AI research", "Machine learning"]
    doc_embs = service.embed_documents(docs)

    # Image embeddings (same space!)
    # image_embs = service.embed_images(["photo.jpg"])
```

### Local Model Service (sentence-transformers)

```python
"""Local embedding service with GPU support and model caching."""

from dataclasses import dataclass
from typing import Literal
import torch
from sentence_transformers import SentenceTransformer


@dataclass
class LocalEmbeddingConfig:
    """Configuration for local embeddings."""
    model_name: str = "BAAI/bge-large-en-v1.5"
    device: Literal["cuda", "cpu", "auto"] = "auto"
    batch_size: int = 32
    normalize: bool = True
    trust_remote_code: bool = False


class LocalEmbeddingService:
    """Local embedding service with GPU acceleration."""

    _model_cache: dict[str, SentenceTransformer] = {}

    def __init__(self, config: LocalEmbeddingConfig | None = None):
        self.config = config or LocalEmbeddingConfig()
        self.device = self._resolve_device()
        self.model = self._load_model()

    def _resolve_device(self) -> str:
        """Resolve device to use."""
        if self.config.device == "auto":
            return "cuda" if torch.cuda.is_available() else "cpu"
        return self.config.device

    def _load_model(self) -> SentenceTransformer:
        """Load model with caching."""
        cache_key = f"{self.config.model_name}:{self.device}"

        if cache_key not in self._model_cache:
            print(f"Loading model {self.config.model_name} on {self.device}...")
            self._model_cache[cache_key] = SentenceTransformer(
                self.config.model_name,
                device=self.device,
                trust_remote_code=self.config.trust_remote_code
            )

        return self._model_cache[cache_key]

    def embed(self, texts: list[str], show_progress: bool = False) -> list[list[float]]:
        """Embed texts."""
        embeddings = self.model.encode(
            texts,
            batch_size=self.config.batch_size,
            show_progress_bar=show_progress,
            convert_to_numpy=True,
            normalize_embeddings=self.config.normalize
        )
        return embeddings.tolist()

    def embed_single(self, text: str) -> list[float]:
        """Embed single text."""
        return self.embed([text])[0]


# Popular model presets
class ModelPresets:
    """Common model configurations."""

    @staticmethod
    def fast() -> LocalEmbeddingConfig:
        """Fast inference, lower quality."""
        return LocalEmbeddingConfig(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            batch_size=64
        )

    @staticmethod
    def balanced() -> LocalEmbeddingConfig:
        """Balanced quality and speed."""
        return LocalEmbeddingConfig(
            model_name="BAAI/bge-large-en-v1.5",
            batch_size=32
        )

    @staticmethod
    def best_quality() -> LocalEmbeddingConfig:
        """Best quality, slower."""
        return LocalEmbeddingConfig(
            model_name="BAAI/bge-m3",
            batch_size=16
        )

    @staticmethod
    def long_context() -> LocalEmbeddingConfig:
        """8K token context."""
        return LocalEmbeddingConfig(
            model_name="nomic-ai/nomic-embed-text-v2-moe",
            trust_remote_code=True,
            batch_size=16
        )


# Usage
if __name__ == "__main__":
    # Fast model
    service = LocalEmbeddingService(ModelPresets.fast())
    emb = service.embed_single("Hello world")
    print(f"Fast model dims: {len(emb)}")

    # Best quality
    service = LocalEmbeddingService(ModelPresets.best_quality())
    emb = service.embed_single("Hello world")
    print(f"BGE-M3 dims: {len(emb)}")
```

---

## Batch Processing Templates

### Async Batch Processor

```python
"""Async batch processor for high-throughput embedding generation."""

import asyncio
from dataclasses import dataclass
from typing import Callable, Awaitable
from openai import AsyncOpenAI


@dataclass
class AsyncBatchConfig:
    """Configuration for async batch processing."""
    batch_size: int = 100
    max_concurrent: int = 5
    rate_limit_delay: float = 0.1


class AsyncBatchProcessor:
    """Async batch processor with rate limiting."""

    def __init__(
        self,
        embed_fn: Callable[[list[str]], Awaitable[list[list[float]]]],
        config: AsyncBatchConfig | None = None
    ):
        self.embed_fn = embed_fn
        self.config = config or AsyncBatchConfig()

    async def process(
        self,
        texts: list[str],
        progress_callback: Callable[[int, int], None] | None = None
    ) -> list[list[float]]:
        """Process texts with controlled concurrency."""
        semaphore = asyncio.Semaphore(self.config.max_concurrent)

        async def process_batch(
            batch: list[str],
            batch_idx: int
        ) -> tuple[int, list[list[float]]]:
            async with semaphore:
                # Rate limiting
                await asyncio.sleep(self.config.rate_limit_delay * batch_idx)
                result = await self.embed_fn(batch)
                return batch_idx, result

        # Create batches
        batches = [
            texts[i:i + self.config.batch_size]
            for i in range(0, len(texts), self.config.batch_size)
        ]

        # Process with progress tracking
        tasks = [process_batch(batch, idx) for idx, batch in enumerate(batches)]
        results = []

        for coro in asyncio.as_completed(tasks):
            batch_idx, embeddings = await coro
            results.append((batch_idx, embeddings))

            if progress_callback:
                progress_callback(len(results), len(batches))

        # Sort by batch index and flatten
        sorted_results = sorted(results, key=lambda x: x[0])
        return [emb for _, batch_embs in sorted_results for emb in batch_embs]


# OpenAI async embed function
async def openai_embed_async(texts: list[str]) -> list[list[float]]:
    """Async OpenAI embedding function."""
    client = AsyncOpenAI()
    response = await client.embeddings.create(
        input=texts,
        model="text-embedding-3-large"
    )
    sorted_data = sorted(response.data, key=lambda x: x.index)
    return [e.embedding for e in sorted_data]


# Usage
async def main():
    processor = AsyncBatchProcessor(
        embed_fn=openai_embed_async,
        config=AsyncBatchConfig(batch_size=100, max_concurrent=5)
    )

    texts = [f"Document {i}" for i in range(1000)]

    def on_progress(done, total):
        print(f"Progress: {done}/{total} batches")

    embeddings = await processor.process(texts, progress_callback=on_progress)
    print(f"Generated {len(embeddings)} embeddings")


if __name__ == "__main__":
    asyncio.run(main())
```

### Parallel Batch Processor (Threads)

```python
"""Thread-based parallel batch processor."""

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Callable
import time


@dataclass
class ParallelBatchConfig:
    """Configuration for parallel processing."""
    batch_size: int = 100
    max_workers: int = 4
    stagger_delay: float = 0.1


class ParallelBatchProcessor:
    """Thread-based parallel batch processor."""

    def __init__(
        self,
        embed_fn: Callable[[list[str]], list[list[float]]],
        config: ParallelBatchConfig | None = None
    ):
        self.embed_fn = embed_fn
        self.config = config or ParallelBatchConfig()

    def process(self, texts: list[str], show_progress: bool = True) -> list[list[float]]:
        """Process texts in parallel batches."""
        batches = [
            texts[i:i + self.config.batch_size]
            for i in range(0, len(texts), self.config.batch_size)
        ]

        results = [None] * len(batches)

        with ThreadPoolExecutor(max_workers=self.config.max_workers) as executor:
            futures = {
                executor.submit(self._process_batch, batch, idx): idx
                for idx, batch in enumerate(batches)
            }

            completed = 0
            for future in as_completed(futures):
                idx = futures[future]
                results[idx] = future.result()
                completed += 1

                if show_progress:
                    print(f"Progress: {completed}/{len(batches)} batches")

        # Flatten results
        return [emb for batch in results for emb in batch]

    def _process_batch(self, batch: list[str], idx: int) -> list[list[float]]:
        """Process single batch with staggered start."""
        time.sleep(self.config.stagger_delay * idx)
        return self.embed_fn(batch)
```

---

## Caching Templates

### Production Redis Cache

```python
"""Production-ready Redis cache for embeddings."""

import json
import hashlib
from dataclasses import dataclass
from typing import Callable
import redis


@dataclass
class RedisCacheConfig:
    """Configuration for Redis cache."""
    redis_url: str = "redis://localhost:6379"
    ttl_days: int = 30
    prefix: str = "emb"
    max_pipeline_size: int = 100


class RedisEmbeddingCache:
    """Production Redis cache with batch operations."""

    def __init__(self, config: RedisCacheConfig | None = None):
        self.config = config or RedisCacheConfig()
        self.client = redis.from_url(self.config.redis_url)
        self.ttl = 86400 * self.config.ttl_days

    def _key(self, text: str, model: str) -> str:
        """Generate cache key."""
        content = f"{model}:{text}"
        hash_val = hashlib.sha256(content.encode()).hexdigest()
        return f"{self.config.prefix}:{hash_val}"

    def get(self, text: str, model: str) -> list[float] | None:
        """Get single embedding from cache."""
        data = self.client.get(self._key(text, model))
        return json.loads(data) if data else None

    def set(self, text: str, model: str, embedding: list[float]):
        """Set single embedding in cache."""
        self.client.setex(
            self._key(text, model),
            self.ttl,
            json.dumps(embedding)
        )

    def get_batch(
        self,
        texts: list[str],
        model: str
    ) -> dict[int, list[float] | None]:
        """Get multiple embeddings from cache."""
        pipe = self.client.pipeline()
        keys = [self._key(t, model) for t in texts]

        for key in keys:
            pipe.get(key)

        results = pipe.execute()

        return {
            i: json.loads(data) if data else None
            for i, data in enumerate(results)
        }

    def set_batch(
        self,
        texts: list[str],
        model: str,
        embeddings: list[list[float]]
    ):
        """Set multiple embeddings in cache."""
        pipe = self.client.pipeline()

        for text, emb in zip(texts, embeddings):
            key = self._key(text, model)
            pipe.setex(key, self.ttl, json.dumps(emb))

        pipe.execute()

    def get_or_compute_batch(
        self,
        texts: list[str],
        model: str,
        compute_fn: Callable[[list[str]], list[list[float]]]
    ) -> list[list[float]]:
        """Get from cache or compute missing embeddings."""
        # Check cache
        cached = self.get_batch(texts, model)

        # Identify uncached
        uncached_indices = [i for i, v in cached.items() if v is None]
        uncached_texts = [texts[i] for i in uncached_indices]

        # Compute uncached
        if uncached_texts:
            new_embeddings = compute_fn(uncached_texts)

            # Store in cache
            self.set_batch(uncached_texts, model, new_embeddings)

            # Merge results
            for idx, emb in zip(uncached_indices, new_embeddings):
                cached[idx] = emb

        return [cached[i] for i in range(len(texts))]

    def stats(self) -> dict:
        """Get cache statistics."""
        info = self.client.info("stats")
        return {
            "keyspace_hits": info.get("keyspace_hits", 0),
            "keyspace_misses": info.get("keyspace_misses", 0),
            "hit_rate": info.get("keyspace_hits", 0) / (
                info.get("keyspace_hits", 0) + info.get("keyspace_misses", 0) + 1
            )
        }


# Usage
if __name__ == "__main__":
    from openai import OpenAI

    cache = RedisEmbeddingCache()
    client = OpenAI()

    def compute_embeddings(texts: list[str]) -> list[list[float]]:
        response = client.embeddings.create(
            input=texts,
            model="text-embedding-3-large"
        )
        return [e.embedding for e in sorted(response.data, key=lambda x: x.index)]

    texts = ["Hello", "World", "Hello"]  # "Hello" appears twice
    embeddings = cache.get_or_compute_batch(
        texts,
        "text-embedding-3-large",
        compute_embeddings
    )
    print(f"Generated {len(embeddings)} embeddings")
    print(f"Cache stats: {cache.stats()}")
```

### SQLite Cache (Development)

```python
"""SQLite cache for development and small-scale use."""

import json
import hashlib
import sqlite3
from pathlib import Path
from typing import Callable


class SQLiteEmbeddingCache:
    """SQLite-based embedding cache."""

    def __init__(self, db_path: str = ".embedding_cache.db"):
        self.db_path = Path(db_path)
        self._init_db()

    def _init_db(self):
        """Initialize database schema."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS embeddings (
                key TEXT PRIMARY KEY,
                model TEXT,
                embedding TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_model ON embeddings(model)")
        conn.commit()
        conn.close()

    def _key(self, text: str, model: str) -> str:
        content = f"{model}:{text}"
        return hashlib.sha256(content.encode()).hexdigest()

    def get(self, text: str, model: str) -> list[float] | None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute(
            "SELECT embedding FROM embeddings WHERE key = ?",
            (self._key(text, model),)
        )
        row = cursor.fetchone()
        conn.close()
        return json.loads(row[0]) if row else None

    def set(self, text: str, model: str, embedding: list[float]):
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            """INSERT OR REPLACE INTO embeddings (key, model, embedding)
               VALUES (?, ?, ?)""",
            (self._key(text, model), model, json.dumps(embedding))
        )
        conn.commit()
        conn.close()

    def get_or_compute(
        self,
        text: str,
        model: str,
        compute_fn: Callable[[str], list[float]]
    ) -> list[float]:
        cached = self.get(text, model)
        if cached:
            return cached

        embedding = compute_fn(text)
        self.set(text, model, embedding)
        return embedding

    def clear(self, model: str | None = None):
        """Clear cache, optionally for specific model."""
        conn = sqlite3.connect(self.db_path)
        if model:
            conn.execute("DELETE FROM embeddings WHERE model = ?", (model,))
        else:
            conn.execute("DELETE FROM embeddings")
        conn.commit()
        conn.close()
```

---

## Complete Pipeline Templates

### RAG Pipeline

```python
"""Complete RAG pipeline with embedding, indexing, and retrieval."""

from dataclasses import dataclass, field
from typing import Callable
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class RAGConfig:
    """Configuration for RAG pipeline."""
    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k: int = 5
    similarity_threshold: float = 0.7


@dataclass
class Document:
    """Document with content and metadata."""
    content: str
    metadata: dict = field(default_factory=dict)
    embedding: list[float] | None = None


class RAGPipeline:
    """Complete RAG pipeline."""

    def __init__(
        self,
        embed_fn: Callable[[list[str]], list[list[float]]],
        config: RAGConfig | None = None
    ):
        self.embed_fn = embed_fn
        self.config = config or RAGConfig()
        self.documents: list[Document] = []
        self.chunks: list[Document] = []
        self.embeddings: np.ndarray | None = None

    def add_documents(self, documents: list[Document]):
        """Add and process documents."""
        self.documents.extend(documents)

        # Chunk documents
        for doc in documents:
            chunks = self._chunk_text(doc.content)
            for i, chunk in enumerate(chunks):
                self.chunks.append(Document(
                    content=chunk,
                    metadata={
                        **doc.metadata,
                        "chunk_index": i,
                        "total_chunks": len(chunks)
                    }
                ))

        # Generate embeddings
        texts = [c.content for c in self.chunks]
        embeddings = self.embed_fn(texts)

        for chunk, emb in zip(self.chunks, embeddings):
            chunk.embedding = emb

        self.embeddings = np.array(embeddings)

    def retrieve(
        self,
        query: str,
        top_k: int | None = None,
        filter_fn: Callable[[Document], bool] | None = None
    ) -> list[tuple[Document, float]]:
        """Retrieve relevant chunks for query."""
        k = top_k or self.config.top_k

        # Embed query
        query_embedding = np.array(self.embed_fn([query])[0]).reshape(1, -1)

        # Filter if needed
        if filter_fn:
            indices = [i for i, c in enumerate(self.chunks) if filter_fn(c)]
            embeddings = self.embeddings[indices]
            chunks = [self.chunks[i] for i in indices]
        else:
            embeddings = self.embeddings
            chunks = self.chunks

        # Calculate similarities
        similarities = cosine_similarity(query_embedding, embeddings)[0]

        # Get top-k
        top_indices = np.argsort(similarities)[::-1][:k]

        results = []
        for idx in top_indices:
            score = float(similarities[idx])
            if score >= self.config.similarity_threshold:
                results.append((chunks[idx], score))

        return results

    def _chunk_text(self, text: str) -> list[str]:
        """Chunk text into overlapping segments."""
        words = text.split()
        chunks = []
        start = 0

        while start < len(words):
            end = start + self.config.chunk_size
            chunk = " ".join(words[start:end])
            chunks.append(chunk)
            start = end - self.config.chunk_overlap

        return chunks


# Usage
if __name__ == "__main__":
    from openai import OpenAI

    client = OpenAI()

    def embed(texts: list[str]) -> list[list[float]]:
        response = client.embeddings.create(
            input=texts,
            model="text-embedding-3-large",
            dimensions=1024
        )
        return [e.embedding for e in sorted(response.data, key=lambda x: x.index)]

    # Create pipeline
    rag = RAGPipeline(embed, RAGConfig(chunk_size=200, top_k=3))

    # Add documents
    rag.add_documents([
        Document("Python is a programming language...", {"source": "wiki"}),
        Document("Machine learning is a subset of AI...", {"source": "textbook"}),
    ])

    # Retrieve
    results = rag.retrieve("What is Python?")
    for doc, score in results:
        print(f"Score: {score:.4f} | {doc.content[:50]}...")
```

### Document Processing Pipeline

```python
"""Complete document processing pipeline with chunking, deduplication, and embedding."""

from dataclasses import dataclass
from typing import Callable
import hashlib
import tiktoken
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


@dataclass
class ProcessingConfig:
    """Configuration for document processing."""
    max_tokens: int = 500
    overlap_tokens: int = 50
    dedup_threshold: float = 0.95
    model: str = "text-embedding-3-large"


class DocumentProcessor:
    """Document processing pipeline."""

    def __init__(
        self,
        embed_fn: Callable[[list[str]], list[list[float]]],
        config: ProcessingConfig | None = None
    ):
        self.embed_fn = embed_fn
        self.config = config or ProcessingConfig()
        self.encoding = tiktoken.encoding_for_model(self.config.model)

    def process(
        self,
        texts: list[str],
        deduplicate: bool = True
    ) -> tuple[list[str], list[list[float]]]:
        """Process texts: chunk, deduplicate, embed."""
        # 1. Chunk all texts
        all_chunks = []
        for text in texts:
            chunks = self._chunk_by_tokens(text)
            all_chunks.extend(chunks)

        # 2. Deduplicate
        if deduplicate:
            all_chunks = self._deduplicate(all_chunks)

        # 3. Embed
        embeddings = self.embed_fn(all_chunks)

        return all_chunks, embeddings

    def _chunk_by_tokens(self, text: str) -> list[str]:
        """Chunk text by token count."""
        tokens = self.encoding.encode(text)
        chunks = []
        start = 0

        while start < len(tokens):
            end = min(start + self.config.max_tokens, len(tokens))
            chunk_tokens = tokens[start:end]
            chunk_text = self.encoding.decode(chunk_tokens)
            chunks.append(chunk_text)
            start = end - self.config.overlap_tokens

        return chunks

    def _deduplicate(self, texts: list[str]) -> list[str]:
        """Remove near-duplicate texts using TF-IDF."""
        if len(texts) <= 1:
            return texts

        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(texts)

        unique_indices = [0]
        for i in range(1, len(texts)):
            current_vec = tfidf_matrix[i]
            existing_vecs = tfidf_matrix[unique_indices]
            similarities = cosine_similarity(current_vec, existing_vecs)[0]

            if max(similarities) < self.config.dedup_threshold:
                unique_indices.append(i)

        return [texts[i] for i in unique_indices]

    def estimate_cost(self, texts: list[str], cost_per_million: float = 0.13) -> dict:
        """Estimate embedding cost."""
        total_tokens = sum(len(self.encoding.encode(t)) for t in texts)
        cost = (total_tokens / 1_000_000) * cost_per_million

        return {
            "total_texts": len(texts),
            "total_tokens": total_tokens,
            "estimated_cost_usd": round(cost, 4)
        }
```

---

## Configuration Templates

### Environment Configuration

```python
"""Configuration management for embedding services."""

import os
from dataclasses import dataclass, field
from typing import Literal


@dataclass
class EmbeddingServiceConfig:
    """Main configuration for embedding services."""

    # Provider selection
    provider: Literal["openai", "voyage", "cohere", "local"] = "openai"

    # OpenAI settings
    openai_model: str = "text-embedding-3-large"
    openai_dimensions: int | None = None

    # Voyage settings
    voyage_model: str = "voyage-3.5"
    voyage_dimensions: int = 1024

    # Cohere settings
    cohere_model: str = "embed-v4"
    cohere_dimensions: int = 1024

    # Local settings
    local_model: str = "BAAI/bge-large-en-v1.5"
    local_device: str = "auto"

    # Processing settings
    batch_size: int = 100
    max_retries: int = 5
    chunk_size: int = 500
    chunk_overlap: int = 50

    # Cache settings
    cache_enabled: bool = True
    cache_ttl_days: int = 30
    redis_url: str = "redis://localhost:6379"

    @classmethod
    def from_env(cls) -> "EmbeddingServiceConfig":
        """Load configuration from environment variables."""
        return cls(
            provider=os.getenv("EMBEDDING_PROVIDER", "openai"),
            openai_model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large"),
            openai_dimensions=int(os.getenv("OPENAI_EMBEDDING_DIMENSIONS", 0)) or None,
            voyage_model=os.getenv("VOYAGE_EMBEDDING_MODEL", "voyage-3.5"),
            voyage_dimensions=int(os.getenv("VOYAGE_EMBEDDING_DIMENSIONS", 1024)),
            cohere_model=os.getenv("COHERE_EMBEDDING_MODEL", "embed-v4"),
            cohere_dimensions=int(os.getenv("COHERE_EMBEDDING_DIMENSIONS", 1024)),
            local_model=os.getenv("LOCAL_EMBEDDING_MODEL", "BAAI/bge-large-en-v1.5"),
            local_device=os.getenv("LOCAL_EMBEDDING_DEVICE", "auto"),
            batch_size=int(os.getenv("EMBEDDING_BATCH_SIZE", 100)),
            max_retries=int(os.getenv("EMBEDDING_MAX_RETRIES", 5)),
            chunk_size=int(os.getenv("EMBEDDING_CHUNK_SIZE", 500)),
            chunk_overlap=int(os.getenv("EMBEDDING_CHUNK_OVERLAP", 50)),
            cache_enabled=os.getenv("EMBEDDING_CACHE_ENABLED", "true").lower() == "true",
            cache_ttl_days=int(os.getenv("EMBEDDING_CACHE_TTL_DAYS", 30)),
            redis_url=os.getenv("REDIS_URL", "redis://localhost:6379"),
        )


# Environment variable template (.env)
ENV_TEMPLATE = """
# Embedding Provider: openai, voyage, cohere, local
EMBEDDING_PROVIDER=openai

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_EMBEDDING_MODEL=text-embedding-3-large
OPENAI_EMBEDDING_DIMENSIONS=1024

# Voyage AI
VOYAGE_API_KEY=pa-...
VOYAGE_EMBEDDING_MODEL=voyage-3.5
VOYAGE_EMBEDDING_DIMENSIONS=1024

# Cohere
COHERE_API_KEY=...
COHERE_EMBEDDING_MODEL=embed-v4
COHERE_EMBEDDING_DIMENSIONS=1024

# Local
LOCAL_EMBEDDING_MODEL=BAAI/bge-large-en-v1.5
LOCAL_EMBEDDING_DEVICE=auto

# Processing
EMBEDDING_BATCH_SIZE=100
EMBEDDING_MAX_RETRIES=5
EMBEDDING_CHUNK_SIZE=500
EMBEDDING_CHUNK_OVERLAP=50

# Cache
EMBEDDING_CACHE_ENABLED=true
EMBEDDING_CACHE_TTL_DAYS=30
REDIS_URL=redis://localhost:6379
"""
```

---

## Testing Templates

### Embedding Service Tests

```python
"""Test templates for embedding services."""

import pytest
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class TestEmbeddingService:
    """Test suite for embedding services."""

    @pytest.fixture
    def service(self):
        """Create service instance. Override in subclass."""
        raise NotImplementedError

    def test_single_embedding_returns_vector(self, service):
        """Test single embedding returns valid vector."""
        text = "Hello world"
        embedding = service.embed_single(text)

        assert isinstance(embedding, list)
        assert len(embedding) > 0
        assert all(isinstance(x, float) for x in embedding)

    def test_batch_embedding_preserves_order(self, service):
        """Test batch embedding preserves input order."""
        texts = ["First", "Second", "Third"]
        embeddings = service.embed_batch(texts)

        assert len(embeddings) == len(texts)

    def test_similar_texts_have_high_similarity(self, service):
        """Test semantic similarity is captured."""
        texts = [
            "Python is a programming language",
            "Python is a language for coding",
            "The weather is nice today"
        ]
        embeddings = service.embed_batch(texts)

        # Similar texts should have higher similarity
        sim_01 = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        sim_02 = cosine_similarity([embeddings[0]], [embeddings[2]])[0][0]

        assert sim_01 > sim_02, "Similar texts should have higher similarity"

    def test_empty_string_handled(self, service):
        """Test empty string is handled gracefully."""
        embedding = service.embed_single("")
        assert embedding is not None

    def test_long_text_handled(self, service):
        """Test long text is handled (may be truncated)."""
        long_text = "word " * 10000
        embedding = service.embed_single(long_text)
        assert embedding is not None

    def test_unicode_handled(self, service):
        """Test Unicode characters are handled."""
        texts = ["Hello", "Bonjour", "Hola"]
        embeddings = service.embed_batch(texts)
        assert len(embeddings) == 3


class TestEmbeddingCache:
    """Test suite for caching layer."""

    @pytest.fixture
    def cache(self):
        """Create cache instance. Override in subclass."""
        raise NotImplementedError

    def test_set_and_get(self, cache):
        """Test basic set and get."""
        text = "test text"
        model = "test-model"
        embedding = [0.1, 0.2, 0.3]

        cache.set(text, model, embedding)
        retrieved = cache.get(text, model)

        assert retrieved == embedding

    def test_get_nonexistent_returns_none(self, cache):
        """Test getting nonexistent key returns None."""
        result = cache.get("nonexistent", "model")
        assert result is None

    def test_different_models_separate_cache(self, cache):
        """Test different models have separate cache entries."""
        text = "same text"
        emb1 = [0.1, 0.2]
        emb2 = [0.3, 0.4]

        cache.set(text, "model1", emb1)
        cache.set(text, "model2", emb2)

        assert cache.get(text, "model1") == emb1
        assert cache.get(text, "model2") == emb2


class TestRetrieval:
    """Test suite for retrieval quality."""

    def test_recall_at_k(self, search_fn, test_data):
        """Test recall@k metric."""
        queries, documents, relevance = test_data

        recalls = []
        for query, relevant_docs in zip(queries, relevance):
            results = search_fn(query, top_k=10)
            result_ids = [r["id"] for r in results]

            hits = len(set(result_ids) & set(relevant_docs))
            recall = hits / len(relevant_docs)
            recalls.append(recall)

        avg_recall = np.mean(recalls)
        assert avg_recall > 0.7, f"Recall@10 too low: {avg_recall}"

    def test_mrr(self, search_fn, test_data):
        """Test Mean Reciprocal Rank."""
        queries, documents, relevance = test_data

        mrrs = []
        for query, relevant_docs in zip(queries, relevance):
            results = search_fn(query, top_k=10)

            for rank, result in enumerate(results, 1):
                if result["id"] in relevant_docs:
                    mrrs.append(1 / rank)
                    break
            else:
                mrrs.append(0)

        avg_mrr = np.mean(mrrs)
        assert avg_mrr > 0.5, f"MRR too low: {avg_mrr}"
```

---

*For more examples, see the [examples.md](examples.md) file for provider-specific code samples.*
