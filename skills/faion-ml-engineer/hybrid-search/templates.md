# Hybrid Search Templates

Production-ready templates for hybrid search pipelines, configurations, and testing.

## Table of Contents

1. [Pipeline Templates](#pipeline-templates)
2. [Configuration Templates](#configuration-templates)
3. [Schema Templates](#schema-templates)
4. [API Templates](#api-templates)
5. [Testing Templates](#testing-templates)
6. [Monitoring Templates](#monitoring-templates)
7. [Deployment Templates](#deployment-templates)

---

## Pipeline Templates

### Complete Hybrid Search Service

```python
"""
hybrid_search_service.py

Production-ready hybrid search service with:
- Async support
- Caching
- Reranking
- Metrics
- Error handling
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional, Protocol
from enum import Enum
import asyncio
import logging
import time
from collections import defaultdict

import numpy as np

logger = logging.getLogger(__name__)


# ============================================================================
# Configuration
# ============================================================================

class FusionMethod(Enum):
    RRF = "rrf"
    LINEAR = "linear"
    CONVEX = "convex"


@dataclass
class HybridSearchConfig:
    """Configuration for hybrid search."""

    # Fusion settings
    fusion_method: FusionMethod = FusionMethod.RRF
    alpha: float = 0.5  # For linear/convex: 0=BM25, 1=vector
    rrf_k: int = 60

    # BM25 settings
    bm25_k1: float = 1.5
    bm25_b: float = 0.75

    # Retrieval settings
    initial_k: int = 100  # Candidates before fusion
    final_k: int = 10  # Final results

    # Reranking
    enable_reranking: bool = False
    rerank_model: str = "rerank-english-v3.0"
    rerank_top_n: int = 100

    # Caching
    enable_cache: bool = True
    cache_ttl: int = 900  # 15 minutes

    # Performance
    timeout_ms: int = 5000
    enable_async: bool = True

    # Query-adaptive alpha
    enable_adaptive_alpha: bool = False


# ============================================================================
# Interfaces
# ============================================================================

class EmbeddingProvider(Protocol):
    """Interface for embedding providers."""

    async def embed(self, text: str) -> list[float]:
        """Embed a single text."""
        ...

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple texts."""
        ...


class VectorStore(Protocol):
    """Interface for vector stores."""

    async def search(
        self,
        vector: list[float],
        k: int,
        filters: Optional[dict] = None
    ) -> list[dict]:
        """Vector similarity search."""
        ...

    async def upsert(self, documents: list[dict]) -> None:
        """Upsert documents with vectors."""
        ...


class KeywordStore(Protocol):
    """Interface for keyword stores."""

    async def search(
        self,
        query: str,
        k: int,
        filters: Optional[dict] = None
    ) -> list[dict]:
        """Keyword search (BM25/full-text)."""
        ...

    async def upsert(self, documents: list[dict]) -> None:
        """Upsert documents for keyword search."""
        ...


class Reranker(Protocol):
    """Interface for rerankers."""

    async def rerank(
        self,
        query: str,
        documents: list[dict],
        top_n: int
    ) -> list[dict]:
        """Rerank documents by relevance to query."""
        ...


class Cache(Protocol):
    """Interface for caching."""

    async def get(self, key: str) -> Optional[Any]:
        """Get cached value."""
        ...

    async def set(self, key: str, value: Any, ttl: int) -> None:
        """Set cached value with TTL."""
        ...


# ============================================================================
# Fusion Implementations
# ============================================================================

class FusionStrategy(ABC):
    """Base class for fusion strategies."""

    @abstractmethod
    def fuse(
        self,
        vector_results: list[dict],
        keyword_results: list[dict],
        **kwargs
    ) -> list[dict]:
        """Fuse two result sets."""
        pass


class RRFFusion(FusionStrategy):
    """Reciprocal Rank Fusion."""

    def __init__(self, k: int = 60):
        self.k = k

    def fuse(
        self,
        vector_results: list[dict],
        keyword_results: list[dict],
        **kwargs
    ) -> list[dict]:
        rrf_scores: dict[str, float] = defaultdict(float)
        doc_map: dict[str, dict] = {}

        for rank, doc in enumerate(vector_results):
            doc_id = doc["id"]
            rrf_scores[doc_id] += 1.0 / (self.k + rank + 1)
            doc_map[doc_id] = doc

        for rank, doc in enumerate(keyword_results):
            doc_id = doc["id"]
            rrf_scores[doc_id] += 1.0 / (self.k + rank + 1)
            if doc_id not in doc_map:
                doc_map[doc_id] = doc

        sorted_ids = sorted(rrf_scores.keys(), key=lambda x: rrf_scores[x], reverse=True)

        return [
            {**doc_map[doc_id], "score": rrf_scores[doc_id], "fusion": "rrf"}
            for doc_id in sorted_ids
        ]


class LinearFusion(FusionStrategy):
    """Weighted linear combination with score normalization."""

    def __init__(self, alpha: float = 0.5):
        self.alpha = alpha

    def _normalize(self, scores: list[float]) -> list[float]:
        """Min-max normalization."""
        if not scores:
            return scores
        min_s, max_s = min(scores), max(scores)
        if max_s - min_s == 0:
            return [0.5] * len(scores)
        return [(s - min_s) / (max_s - min_s) for s in scores]

    def fuse(
        self,
        vector_results: list[dict],
        keyword_results: list[dict],
        **kwargs
    ) -> list[dict]:
        alpha = kwargs.get("alpha", self.alpha)

        # Normalize scores
        vector_scores = self._normalize([d["score"] for d in vector_results])
        keyword_scores = self._normalize([d["score"] for d in keyword_results])

        # Build normalized score maps
        vector_map = {d["id"]: (d, s) for d, s in zip(vector_results, vector_scores)}
        keyword_map = {d["id"]: (d, s) for d, s in zip(keyword_results, keyword_scores)}

        # Combine
        all_ids = set(vector_map.keys()) | set(keyword_map.keys())
        combined = []

        for doc_id in all_ids:
            v_score = vector_map.get(doc_id, (None, 0))[1]
            k_score = keyword_map.get(doc_id, (None, 0))[1]
            hybrid_score = alpha * v_score + (1 - alpha) * k_score

            doc = vector_map.get(doc_id, keyword_map.get(doc_id))[0]
            combined.append({
                **doc,
                "score": hybrid_score,
                "vector_score": v_score,
                "keyword_score": k_score,
                "fusion": "linear",
                "alpha": alpha
            })

        combined.sort(key=lambda x: x["score"], reverse=True)
        return combined


# ============================================================================
# Main Service
# ============================================================================

@dataclass
class SearchMetrics:
    """Metrics for a single search."""
    total_ms: float = 0
    vector_ms: float = 0
    keyword_ms: float = 0
    fusion_ms: float = 0
    rerank_ms: float = 0
    cache_hit: bool = False
    vector_count: int = 0
    keyword_count: int = 0
    final_count: int = 0


class HybridSearchService:
    """
    Production hybrid search service.

    Usage:
        service = HybridSearchService(
            config=HybridSearchConfig(),
            embedding_provider=OpenAIEmbeddings(),
            vector_store=QdrantStore(),
            keyword_store=ElasticsearchStore(),
            reranker=CohereReranker(),
            cache=RedisCache()
        )

        results = await service.search("my query", filters={"source": "docs"})
    """

    def __init__(
        self,
        config: HybridSearchConfig,
        embedding_provider: EmbeddingProvider,
        vector_store: VectorStore,
        keyword_store: KeywordStore,
        reranker: Optional[Reranker] = None,
        cache: Optional[Cache] = None
    ):
        self.config = config
        self.embeddings = embedding_provider
        self.vector_store = vector_store
        self.keyword_store = keyword_store
        self.reranker = reranker
        self.cache = cache

        # Initialize fusion strategy
        if config.fusion_method == FusionMethod.RRF:
            self.fusion = RRFFusion(k=config.rrf_k)
        else:
            self.fusion = LinearFusion(alpha=config.alpha)

    def _cache_key(self, query: str, filters: Optional[dict]) -> str:
        """Generate cache key."""
        import hashlib
        import json
        key_data = {"q": query, "f": filters or {}, "a": self.config.alpha}
        return f"hybrid:{hashlib.md5(json.dumps(key_data, sort_keys=True).encode()).hexdigest()}"

    def _determine_alpha(self, query: str) -> float:
        """Query-adaptive alpha selection."""
        if not self.config.enable_adaptive_alpha:
            return self.config.alpha

        has_quotes = '"' in query
        has_codes = any(c.isdigit() for c in query)
        is_short = len(query.split()) <= 3
        has_operators = any(op in query for op in ['AND', 'OR', 'NOT'])

        if has_quotes or has_operators:
            return 0.2  # Strong keyword preference
        elif has_codes:
            return 0.3
        elif is_short:
            return 0.5
        else:
            return 0.7  # Semantic preference

    async def search(
        self,
        query: str,
        filters: Optional[dict] = None,
        k: Optional[int] = None,
        alpha: Optional[float] = None
    ) -> tuple[list[dict], SearchMetrics]:
        """
        Execute hybrid search.

        Args:
            query: Search query
            filters: Optional metadata filters
            k: Override final_k from config
            alpha: Override alpha from config

        Returns:
            Tuple of (results, metrics)
        """
        start_time = time.perf_counter()
        metrics = SearchMetrics()

        final_k = k or self.config.final_k
        search_alpha = alpha or self._determine_alpha(query)

        # Check cache
        if self.config.enable_cache and self.cache:
            cache_key = self._cache_key(query, filters)
            cached = await self.cache.get(cache_key)
            if cached:
                metrics.cache_hit = True
                metrics.total_ms = (time.perf_counter() - start_time) * 1000
                return cached, metrics

        # Get query embedding
        query_vector = await self.embeddings.embed(query)

        # Parallel retrieval
        if self.config.enable_async:
            vector_task = asyncio.create_task(
                self._timed_vector_search(query_vector, filters)
            )
            keyword_task = asyncio.create_task(
                self._timed_keyword_search(query, filters)
            )

            (vector_results, vector_ms), (keyword_results, keyword_ms) = await asyncio.gather(
                vector_task, keyword_task
            )
        else:
            vector_results, vector_ms = await self._timed_vector_search(query_vector, filters)
            keyword_results, keyword_ms = await self._timed_keyword_search(query, filters)

        metrics.vector_ms = vector_ms
        metrics.keyword_ms = keyword_ms
        metrics.vector_count = len(vector_results)
        metrics.keyword_count = len(keyword_results)

        # Fusion
        fusion_start = time.perf_counter()
        fused_results = self.fusion.fuse(
            vector_results,
            keyword_results,
            alpha=search_alpha
        )
        metrics.fusion_ms = (time.perf_counter() - fusion_start) * 1000

        # Reranking
        if self.config.enable_reranking and self.reranker:
            rerank_start = time.perf_counter()
            candidates = fused_results[:self.config.rerank_top_n]
            fused_results = await self.reranker.rerank(query, candidates, final_k)
            metrics.rerank_ms = (time.perf_counter() - rerank_start) * 1000
        else:
            fused_results = fused_results[:final_k]

        metrics.final_count = len(fused_results)
        metrics.total_ms = (time.perf_counter() - start_time) * 1000

        # Cache results
        if self.config.enable_cache and self.cache:
            await self.cache.set(cache_key, fused_results, self.config.cache_ttl)

        return fused_results, metrics

    async def _timed_vector_search(
        self,
        vector: list[float],
        filters: Optional[dict]
    ) -> tuple[list[dict], float]:
        """Vector search with timing."""
        start = time.perf_counter()
        results = await self.vector_store.search(vector, self.config.initial_k, filters)
        elapsed = (time.perf_counter() - start) * 1000
        return results, elapsed

    async def _timed_keyword_search(
        self,
        query: str,
        filters: Optional[dict]
    ) -> tuple[list[dict], float]:
        """Keyword search with timing."""
        start = time.perf_counter()
        results = await self.keyword_store.search(query, self.config.initial_k, filters)
        elapsed = (time.perf_counter() - start) * 1000
        return results, elapsed


# ============================================================================
# Provider Implementations (Templates)
# ============================================================================

class OpenAIEmbeddings:
    """OpenAI embedding provider template."""

    def __init__(self, model: str = "text-embedding-3-small"):
        import openai
        self.client = openai.AsyncOpenAI()
        self.model = model

    async def embed(self, text: str) -> list[float]:
        response = await self.client.embeddings.create(
            model=self.model,
            input=text
        )
        return response.data[0].embedding

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        response = await self.client.embeddings.create(
            model=self.model,
            input=texts
        )
        return [e.embedding for e in response.data]


class CohereReranker:
    """Cohere reranker template."""

    def __init__(self, model: str = "rerank-english-v3.0"):
        import cohere
        self.client = cohere.AsyncClient()
        self.model = model

    async def rerank(
        self,
        query: str,
        documents: list[dict],
        top_n: int
    ) -> list[dict]:
        if not documents:
            return []

        response = await self.client.rerank(
            model=self.model,
            query=query,
            documents=[d.get("content", "") for d in documents],
            top_n=top_n
        )

        return [
            {**documents[r.index], "score": r.relevance_score, "reranked": True}
            for r in response.results
        ]
```

### Indexing Pipeline Template

```python
"""
indexing_pipeline.py

Template for document indexing pipeline with:
- Chunking
- Embedding
- Dual indexing (vector + keyword)
- Progress tracking
- Error handling
"""

from dataclasses import dataclass
from typing import AsyncIterator, Callable, Optional
import asyncio
import logging
from pathlib import Path
import hashlib

logger = logging.getLogger(__name__)


@dataclass
class Document:
    """Document representation."""
    id: str
    content: str
    title: Optional[str] = None
    source: Optional[str] = None
    metadata: Optional[dict] = None


@dataclass
class Chunk:
    """Chunk representation."""
    id: str
    doc_id: str
    content: str
    chunk_index: int
    metadata: Optional[dict] = None
    embedding: Optional[list[float]] = None


@dataclass
class IndexingConfig:
    """Indexing configuration."""
    # Chunking
    chunk_size: int = 512
    chunk_overlap: int = 50
    min_chunk_size: int = 100

    # Embedding
    embedding_model: str = "text-embedding-3-small"
    embedding_batch_size: int = 100
    embedding_dimensions: int = 1536

    # Indexing
    upsert_batch_size: int = 100
    max_concurrent_batches: int = 5

    # Progress
    progress_callback: Optional[Callable[[int, int], None]] = None


class TextChunker:
    """Text chunking with overlap."""

    def __init__(self, config: IndexingConfig):
        self.config = config

    def chunk_document(self, doc: Document) -> list[Chunk]:
        """Split document into chunks."""
        text = doc.content
        chunks = []
        start = 0
        chunk_index = 0

        while start < len(text):
            # Find chunk end
            end = start + self.config.chunk_size

            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence end
                for sep in ['. ', '.\n', '? ', '! ', '\n\n']:
                    last_sep = text[start:end].rfind(sep)
                    if last_sep > self.config.min_chunk_size:
                        end = start + last_sep + len(sep)
                        break

            chunk_text = text[start:end].strip()

            if len(chunk_text) >= self.config.min_chunk_size:
                chunk_id = f"{doc.id}_chunk_{chunk_index}"
                chunks.append(Chunk(
                    id=chunk_id,
                    doc_id=doc.id,
                    content=chunk_text,
                    chunk_index=chunk_index,
                    metadata={
                        "title": doc.title,
                        "source": doc.source,
                        **(doc.metadata or {})
                    }
                ))
                chunk_index += 1

            # Move to next chunk with overlap
            start = end - self.config.chunk_overlap
            if start <= 0:
                start = end

        return chunks


class IndexingPipeline:
    """
    Document indexing pipeline.

    Usage:
        pipeline = IndexingPipeline(
            config=IndexingConfig(),
            embedding_provider=OpenAIEmbeddings(),
            vector_store=QdrantStore(),
            keyword_store=ElasticsearchStore()
        )

        await pipeline.index_documents(documents)
    """

    def __init__(
        self,
        config: IndexingConfig,
        embedding_provider,
        vector_store,
        keyword_store
    ):
        self.config = config
        self.embeddings = embedding_provider
        self.vector_store = vector_store
        self.keyword_store = keyword_store
        self.chunker = TextChunker(config)

    async def index_documents(
        self,
        documents: list[Document],
        on_progress: Optional[Callable[[int, int, str], None]] = None
    ) -> dict:
        """
        Index documents through the pipeline.

        Returns:
            Statistics about the indexing run.
        """
        stats = {
            "total_documents": len(documents),
            "total_chunks": 0,
            "embedded": 0,
            "indexed": 0,
            "errors": []
        }

        # Phase 1: Chunking
        if on_progress:
            on_progress(0, len(documents), "Chunking documents...")

        all_chunks = []
        for i, doc in enumerate(documents):
            try:
                chunks = self.chunker.chunk_document(doc)
                all_chunks.extend(chunks)
            except Exception as e:
                stats["errors"].append({"doc_id": doc.id, "phase": "chunking", "error": str(e)})
                logger.error(f"Chunking failed for {doc.id}: {e}")

            if on_progress and (i + 1) % 100 == 0:
                on_progress(i + 1, len(documents), f"Chunked {i + 1}/{len(documents)} documents")

        stats["total_chunks"] = len(all_chunks)

        # Phase 2: Embedding
        if on_progress:
            on_progress(0, len(all_chunks), "Generating embeddings...")

        embedded_chunks = await self._embed_chunks(all_chunks, on_progress)
        stats["embedded"] = len(embedded_chunks)

        # Phase 3: Indexing
        if on_progress:
            on_progress(0, len(embedded_chunks), "Indexing chunks...")

        indexed = await self._index_chunks(embedded_chunks, on_progress)
        stats["indexed"] = indexed

        return stats

    async def _embed_chunks(
        self,
        chunks: list[Chunk],
        on_progress: Optional[Callable]
    ) -> list[Chunk]:
        """Generate embeddings for chunks in batches."""
        embedded = []
        batch_size = self.config.embedding_batch_size

        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            texts = [c.content for c in batch]

            try:
                embeddings = await self.embeddings.embed_batch(texts)
                for chunk, embedding in zip(batch, embeddings):
                    chunk.embedding = embedding
                    embedded.append(chunk)
            except Exception as e:
                logger.error(f"Embedding batch failed: {e}")
                for chunk in batch:
                    # Mark as failed but continue
                    pass

            if on_progress:
                on_progress(min(i + batch_size, len(chunks)), len(chunks), "Embedding...")

        return embedded

    async def _index_chunks(
        self,
        chunks: list[Chunk],
        on_progress: Optional[Callable]
    ) -> int:
        """Index chunks to vector and keyword stores."""
        batch_size = self.config.upsert_batch_size
        indexed = 0

        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]

            # Prepare documents for indexing
            docs = [
                {
                    "id": c.id,
                    "content": c.content,
                    "embedding": c.embedding,
                    "metadata": c.metadata,
                    "doc_id": c.doc_id,
                    "chunk_index": c.chunk_index
                }
                for c in batch
            ]

            # Parallel indexing to both stores
            try:
                await asyncio.gather(
                    self.vector_store.upsert(docs),
                    self.keyword_store.upsert(docs)
                )
                indexed += len(batch)
            except Exception as e:
                logger.error(f"Indexing batch failed: {e}")

            if on_progress:
                on_progress(min(i + batch_size, len(chunks)), len(chunks), "Indexing...")

        return indexed

    async def delete_document(self, doc_id: str) -> bool:
        """Delete document and all its chunks."""
        try:
            await asyncio.gather(
                self.vector_store.delete_by_filter({"doc_id": doc_id}),
                self.keyword_store.delete_by_filter({"doc_id": doc_id})
            )
            return True
        except Exception as e:
            logger.error(f"Delete failed for {doc_id}: {e}")
            return False

    async def reindex_document(self, doc: Document) -> dict:
        """Delete and re-index a document."""
        await self.delete_document(doc.id)
        return await self.index_documents([doc])
```

---

## Configuration Templates

### Environment Configuration

```yaml
# config/hybrid-search.yaml

# Environment: development | staging | production
environment: production

# Vector Store Configuration
vector_store:
  provider: qdrant  # qdrant | weaviate | pinecone | elasticsearch | pgvector
  host: ${VECTOR_STORE_HOST:localhost}
  port: ${VECTOR_STORE_PORT:6333}
  api_key: ${VECTOR_STORE_API_KEY:}
  collection: documents

  # HNSW index parameters
  hnsw:
    m: 16
    ef_construct: 100
    ef: 100

# Keyword Store Configuration
keyword_store:
  provider: elasticsearch  # elasticsearch | opensearch | typesense
  host: ${KEYWORD_STORE_HOST:localhost}
  port: ${KEYWORD_STORE_PORT:9200}
  index: documents

  # BM25 parameters
  bm25:
    k1: 1.5
    b: 0.75

# Embedding Configuration
embeddings:
  provider: openai  # openai | cohere | voyage | local
  model: text-embedding-3-small
  dimensions: 1536
  batch_size: 100
  max_retries: 3

# Fusion Configuration
fusion:
  method: rrf  # rrf | linear | convex

  # RRF settings
  rrf_k: 60

  # Linear/convex settings
  alpha: 0.5
  enable_adaptive_alpha: false

# Reranking Configuration
reranking:
  enabled: true
  provider: cohere  # cohere | jina | local
  model: rerank-english-v3.0
  top_n: 100

# Caching Configuration
cache:
  enabled: true
  provider: redis  # redis | memcached | memory
  host: ${REDIS_HOST:localhost}
  port: ${REDIS_PORT:6379}
  ttl: 900  # 15 minutes
  max_size: 10000

# Performance Configuration
performance:
  timeout_ms: 5000
  initial_k: 100
  final_k: 10
  enable_async: true
  max_concurrent_requests: 100

# Monitoring Configuration
monitoring:
  enabled: true
  metrics_port: 9090
  log_level: INFO
  trace_sampling_rate: 0.1
```

### Docker Compose Template

```yaml
# docker-compose.yaml

version: '3.8'

services:
  # Qdrant Vector Store
  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_data:/qdrant/storage
    environment:
      - QDRANT__SERVICE__GRPC_PORT=6334
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:6333/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Elasticsearch for BM25
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    ports:
      - "9200:9200"
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms1g -Xmx1g"
    volumes:
      - es_data:/usr/share/elasticsearch/data
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9200/_cluster/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Redis Cache
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Hybrid Search Service
  hybrid-search:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - VECTOR_STORE_HOST=qdrant
      - KEYWORD_STORE_HOST=elasticsearch
      - REDIS_HOST=redis
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - COHERE_API_KEY=${COHERE_API_KEY}
    depends_on:
      qdrant:
        condition: service_healthy
      elasticsearch:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  qdrant_data:
  es_data:
  redis_data:
```

### Kubernetes Deployment Template

```yaml
# k8s/hybrid-search-deployment.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: hybrid-search
  labels:
    app: hybrid-search
spec:
  replicas: 3
  selector:
    matchLabels:
      app: hybrid-search
  template:
    metadata:
      labels:
        app: hybrid-search
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "9090"
    spec:
      containers:
        - name: hybrid-search
          image: your-registry/hybrid-search:latest
          ports:
            - containerPort: 8000
              name: http
            - containerPort: 9090
              name: metrics
          env:
            - name: VECTOR_STORE_HOST
              value: qdrant.default.svc.cluster.local
            - name: KEYWORD_STORE_HOST
              value: elasticsearch.default.svc.cluster.local
            - name: REDIS_HOST
              value: redis.default.svc.cluster.local
            - name: OPENAI_API_KEY
              valueFrom:
                secretKeyRef:
                  name: api-keys
                  key: openai-api-key
          resources:
            requests:
              memory: "512Mi"
              cpu: "250m"
            limits:
              memory: "2Gi"
              cpu: "1000m"
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 10
            periodSeconds: 30
          readinessProbe:
            httpGet:
              path: /ready
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: hybrid-search
spec:
  selector:
    app: hybrid-search
  ports:
    - name: http
      port: 80
      targetPort: 8000
    - name: metrics
      port: 9090
      targetPort: 9090
  type: ClusterIP
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: hybrid-search-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: hybrid-search
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Pods
      pods:
        metric:
          name: http_requests_per_second
        target:
          type: AverageValue
          averageValue: 100
```

---

## Schema Templates

### Weaviate Schema

```python
# schemas/weaviate_schema.py

WEAVIATE_SCHEMA = {
    "class": "Document",
    "description": "Documents for hybrid search",
    "vectorizer": "text2vec-openai",
    "moduleConfig": {
        "text2vec-openai": {
            "model": "text-embedding-3-small",
            "modelVersion": "3",
            "type": "text",
            "vectorizeClassName": False
        }
    },
    "properties": [
        {
            "name": "content",
            "dataType": ["text"],
            "description": "Document content",
            "moduleConfig": {
                "text2vec-openai": {
                    "skip": False,
                    "vectorizePropertyName": False
                }
            }
        },
        {
            "name": "title",
            "dataType": ["text"],
            "description": "Document title",
            "moduleConfig": {
                "text2vec-openai": {
                    "skip": True
                }
            }
        },
        {
            "name": "source",
            "dataType": ["text"],
            "description": "Document source",
            "indexFilterable": True,
            "indexSearchable": False
        },
        {
            "name": "doc_id",
            "dataType": ["text"],
            "description": "Parent document ID",
            "indexFilterable": True,
            "indexSearchable": False
        },
        {
            "name": "chunk_index",
            "dataType": ["int"],
            "description": "Chunk index within document"
        },
        {
            "name": "created_at",
            "dataType": ["date"],
            "description": "Creation timestamp"
        },
        {
            "name": "metadata",
            "dataType": ["object"],
            "description": "Additional metadata",
            "nestedProperties": [
                {"name": "author", "dataType": ["text"]},
                {"name": "category", "dataType": ["text"]},
                {"name": "tags", "dataType": ["text[]"]}
            ]
        }
    ],
    "invertedIndexConfig": {
        "bm25": {
            "b": 0.75,
            "k1": 1.5
        },
        "stopwords": {
            "preset": "en"
        }
    }
}
```

### Qdrant Schema

```python
# schemas/qdrant_schema.py

from qdrant_client.http import models

QDRANT_COLLECTION_CONFIG = {
    "vectors_config": {
        "dense": models.VectorParams(
            size=1536,
            distance=models.Distance.COSINE,
            on_disk=False
        )
    },
    "sparse_vectors_config": {
        "sparse": models.SparseVectorParams(
            index=models.SparseIndexParams(
                on_disk=False
            )
        )
    },
    "hnsw_config": models.HnswConfigDiff(
        m=16,
        ef_construct=100,
        full_scan_threshold=10000
    ),
    "optimizers_config": models.OptimizersConfigDiff(
        indexing_threshold=20000
    ),
    "shard_number": 2,
    "replication_factor": 1,
    "write_consistency_factor": 1
}

QDRANT_PAYLOAD_SCHEMA = {
    "content": models.PayloadSchemaType.TEXT,
    "title": models.PayloadSchemaType.TEXT,
    "source": models.PayloadSchemaType.KEYWORD,
    "doc_id": models.PayloadSchemaType.KEYWORD,
    "chunk_index": models.PayloadSchemaType.INTEGER,
    "created_at": models.PayloadSchemaType.DATETIME
}

# Create collection with schema
def create_qdrant_collection(client, collection_name: str):
    """Create Qdrant collection with optimized settings."""

    client.create_collection(
        collection_name=collection_name,
        **QDRANT_COLLECTION_CONFIG
    )

    # Create payload indexes
    for field, schema_type in QDRANT_PAYLOAD_SCHEMA.items():
        client.create_payload_index(
            collection_name=collection_name,
            field_name=field,
            field_schema=schema_type
        )
```

### Elasticsearch Schema

```python
# schemas/elasticsearch_schema.py

ELASTICSEARCH_INDEX_SETTINGS = {
    "settings": {
        "number_of_shards": 2,
        "number_of_replicas": 1,
        "analysis": {
            "analyzer": {
                "custom_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "stop",
                        "snowball"
                    ]
                }
            }
        },
        "index": {
            "similarity": {
                "custom_bm25": {
                    "type": "BM25",
                    "k1": 1.5,
                    "b": 0.75
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "content": {
                "type": "text",
                "analyzer": "custom_analyzer",
                "similarity": "custom_bm25"
            },
            "title": {
                "type": "text",
                "analyzer": "custom_analyzer",
                "boost": 2.0
            },
            "embedding": {
                "type": "dense_vector",
                "dims": 1536,
                "index": True,
                "similarity": "cosine"
            },
            "source": {
                "type": "keyword"
            },
            "doc_id": {
                "type": "keyword"
            },
            "chunk_index": {
                "type": "integer"
            },
            "created_at": {
                "type": "date"
            },
            "metadata": {
                "type": "object",
                "properties": {
                    "author": {"type": "keyword"},
                    "category": {"type": "keyword"},
                    "tags": {"type": "keyword"}
                }
            }
        }
    }
}
```

---

## API Templates

### FastAPI Hybrid Search API

```python
# api/main.py

from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import logging

from hybrid_search_service import HybridSearchService, HybridSearchConfig

app = FastAPI(
    title="Hybrid Search API",
    description="Production hybrid search API with BM25 + vector fusion",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000, description="Search query")
    k: int = Field(default=10, ge=1, le=100, description="Number of results")
    alpha: Optional[float] = Field(default=None, ge=0, le=1, description="Override alpha")
    filters: Optional[dict] = Field(default=None, description="Metadata filters")

class SearchResult(BaseModel):
    id: str
    content: str
    score: float
    title: Optional[str] = None
    source: Optional[str] = None
    metadata: Optional[dict] = None

class SearchResponse(BaseModel):
    results: list[SearchResult]
    total: int
    query: str
    latency_ms: float
    fusion_method: str

class HealthResponse(BaseModel):
    status: str
    vector_store: str
    keyword_store: str
    cache: str

# Dependency injection
async def get_search_service() -> HybridSearchService:
    # In production, use proper dependency injection
    return app.state.search_service

# Endpoints
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        vector_store="connected",
        keyword_store="connected",
        cache="connected"
    )

@app.get("/ready")
async def readiness_check():
    """Readiness probe for Kubernetes."""
    # Check actual connections
    return {"ready": True}

@app.post("/search", response_model=SearchResponse)
async def search(
    request: SearchRequest,
    service: HybridSearchService = Depends(get_search_service)
):
    """
    Execute hybrid search.

    Combines BM25 keyword search with vector similarity search
    using configurable fusion (RRF or linear combination).
    """
    try:
        results, metrics = await service.search(
            query=request.query,
            filters=request.filters,
            k=request.k,
            alpha=request.alpha
        )

        return SearchResponse(
            results=[SearchResult(**r) for r in results],
            total=len(results),
            query=request.query,
            latency_ms=metrics.total_ms,
            fusion_method=service.config.fusion_method.value
        )
    except Exception as e:
        logging.error(f"Search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/index")
async def index_documents(
    documents: list[dict],
    service: HybridSearchService = Depends(get_search_service)
):
    """Index documents for search."""
    # Implementation here
    pass

@app.delete("/documents/{doc_id}")
async def delete_document(
    doc_id: str,
    service: HybridSearchService = Depends(get_search_service)
):
    """Delete a document and its chunks."""
    # Implementation here
    pass

# Startup/shutdown
@app.on_event("startup")
async def startup():
    """Initialize search service."""
    config = HybridSearchConfig()
    # Initialize providers and create service
    # app.state.search_service = HybridSearchService(...)

@app.on_event("shutdown")
async def shutdown():
    """Cleanup resources."""
    pass
```

### OpenAPI Schema Extension

```yaml
# openapi-extension.yaml

openapi: 3.1.0
info:
  title: Hybrid Search API
  version: 1.0.0
  description: |
    Production hybrid search API combining BM25 keyword search
    with vector similarity search.

    ## Fusion Methods

    - **RRF (Reciprocal Rank Fusion)**: Combines rankings without score normalization.
      Best for general use cases.
    - **Linear**: Weighted combination of normalized scores. Allows fine-tuning
      the balance between keyword and semantic search.

    ## Alpha Parameter

    When using linear fusion:
    - `alpha=0.0`: Pure BM25 keyword search
    - `alpha=0.5`: Balanced hybrid search
    - `alpha=1.0`: Pure vector semantic search

    ## Filters

    Supports metadata filtering:
    ```json
    {
      "filters": {
        "source": "documentation",
        "category": "api"
      }
    }
    ```

paths:
  /search:
    post:
      tags:
        - Search
      summary: Execute hybrid search
      description: |
        Executes a hybrid search combining BM25 and vector similarity.
        Results are fused using the configured fusion method.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/SearchRequest'
            examples:
              basic:
                summary: Basic search
                value:
                  query: "async database connection"
                  k: 10
              with_filters:
                summary: Search with filters
                value:
                  query: "async database connection"
                  k: 10
                  filters:
                    source: "documentation"
              custom_alpha:
                summary: Custom alpha for keyword preference
                value:
                  query: '"exact phrase" search'
                  k: 10
                  alpha: 0.3
      responses:
        '200':
          description: Successful search
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SearchResponse'
        '400':
          description: Invalid request
        '500':
          description: Server error

components:
  schemas:
    SearchRequest:
      type: object
      required:
        - query
      properties:
        query:
          type: string
          minLength: 1
          maxLength: 1000
          description: Search query string
        k:
          type: integer
          minimum: 1
          maximum: 100
          default: 10
          description: Number of results to return
        alpha:
          type: number
          minimum: 0
          maximum: 1
          nullable: true
          description: Override fusion alpha (0=keyword, 1=vector)
        filters:
          type: object
          additionalProperties: true
          description: Metadata filters
```

---

## Testing Templates

### Unit Tests

```python
# tests/test_fusion.py

import pytest
from hybrid_search_service import RRFFusion, LinearFusion

class TestRRFFusion:
    """Tests for RRF fusion."""

    def test_rrf_basic(self):
        """Test basic RRF fusion."""
        fusion = RRFFusion(k=60)

        vector_results = [
            {"id": "1", "content": "doc1", "score": 0.95},
            {"id": "2", "content": "doc2", "score": 0.85},
            {"id": "3", "content": "doc3", "score": 0.75},
        ]

        keyword_results = [
            {"id": "2", "content": "doc2", "score": 12.5},
            {"id": "1", "content": "doc1", "score": 10.0},
            {"id": "4", "content": "doc4", "score": 8.0},
        ]

        fused = fusion.fuse(vector_results, keyword_results)

        # Doc 2 should be first (rank 1 in keyword, rank 2 in vector)
        assert fused[0]["id"] == "2"

        # All documents should be present
        assert len(fused) == 4

        # Scores should be RRF scores
        assert all(r["score"] > 0 for r in fused)

    def test_rrf_single_source(self):
        """Test RRF with results from only one source."""
        fusion = RRFFusion(k=60)

        vector_results = [
            {"id": "1", "content": "doc1", "score": 0.95},
        ]

        fused = fusion.fuse(vector_results, [])

        assert len(fused) == 1
        assert fused[0]["id"] == "1"

    def test_rrf_empty_inputs(self):
        """Test RRF with empty inputs."""
        fusion = RRFFusion(k=60)

        fused = fusion.fuse([], [])

        assert len(fused) == 0

    def test_rrf_k_parameter(self):
        """Test that k parameter affects ranking."""
        fusion_low_k = RRFFusion(k=1)
        fusion_high_k = RRFFusion(k=100)

        vector_results = [{"id": "1", "content": "doc1", "score": 0.95}]
        keyword_results = [{"id": "1", "content": "doc1", "score": 10.0}]

        fused_low = fusion_low_k.fuse(vector_results, keyword_results)
        fused_high = fusion_high_k.fuse(vector_results, keyword_results)

        # Higher k should produce lower RRF scores
        assert fused_low[0]["score"] > fused_high[0]["score"]


class TestLinearFusion:
    """Tests for linear fusion."""

    def test_linear_balanced(self):
        """Test linear fusion with alpha=0.5."""
        fusion = LinearFusion(alpha=0.5)

        vector_results = [
            {"id": "1", "content": "doc1", "score": 0.9},
            {"id": "2", "content": "doc2", "score": 0.5},
        ]

        keyword_results = [
            {"id": "2", "content": "doc2", "score": 10.0},
            {"id": "1", "content": "doc1", "score": 5.0},
        ]

        fused = fusion.fuse(vector_results, keyword_results)

        # Both docs should be present
        assert len(fused) == 2

        # Scores should be normalized and combined
        assert all(0 <= r["score"] <= 1 for r in fused)

    def test_linear_pure_vector(self):
        """Test linear fusion with alpha=1.0 (pure vector)."""
        fusion = LinearFusion(alpha=1.0)

        vector_results = [
            {"id": "1", "content": "doc1", "score": 0.9},
            {"id": "2", "content": "doc2", "score": 0.5},
        ]

        keyword_results = [
            {"id": "2", "content": "doc2", "score": 10.0},
        ]

        fused = fusion.fuse(vector_results, keyword_results)

        # Doc 1 should be first (highest vector score)
        assert fused[0]["id"] == "1"

    def test_linear_pure_keyword(self):
        """Test linear fusion with alpha=0.0 (pure keyword)."""
        fusion = LinearFusion(alpha=0.0)

        vector_results = [
            {"id": "1", "content": "doc1", "score": 0.9},
        ]

        keyword_results = [
            {"id": "2", "content": "doc2", "score": 10.0},
            {"id": "1", "content": "doc1", "score": 5.0},
        ]

        fused = fusion.fuse(vector_results, keyword_results)

        # Doc 2 should be first (highest keyword score)
        assert fused[0]["id"] == "2"

    def test_linear_normalization(self):
        """Test that scores are properly normalized."""
        fusion = LinearFusion(alpha=0.5)

        # Extreme score differences
        vector_results = [
            {"id": "1", "content": "doc1", "score": 1000.0},
            {"id": "2", "content": "doc2", "score": 1.0},
        ]

        keyword_results = [
            {"id": "1", "content": "doc1", "score": 0.001},
            {"id": "2", "content": "doc2", "score": 0.0001},
        ]

        fused = fusion.fuse(vector_results, keyword_results)

        # All scores should be in [0, 1] after normalization
        assert all(0 <= r["score"] <= 1 for r in fused)
```

### Integration Tests

```python
# tests/test_integration.py

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock

from hybrid_search_service import (
    HybridSearchService,
    HybridSearchConfig,
    FusionMethod
)

@pytest.fixture
def mock_embedding_provider():
    """Mock embedding provider."""
    provider = AsyncMock()
    provider.embed.return_value = [0.1] * 1536
    provider.embed_batch.return_value = [[0.1] * 1536]
    return provider

@pytest.fixture
def mock_vector_store():
    """Mock vector store."""
    store = AsyncMock()
    store.search.return_value = [
        {"id": "1", "content": "vector result 1", "score": 0.95},
        {"id": "2", "content": "vector result 2", "score": 0.85},
    ]
    return store

@pytest.fixture
def mock_keyword_store():
    """Mock keyword store."""
    store = AsyncMock()
    store.search.return_value = [
        {"id": "2", "content": "keyword result 2", "score": 12.5},
        {"id": "3", "content": "keyword result 3", "score": 10.0},
    ]
    return store

@pytest.fixture
def search_service(mock_embedding_provider, mock_vector_store, mock_keyword_store):
    """Create search service with mocks."""
    config = HybridSearchConfig(
        fusion_method=FusionMethod.RRF,
        enable_cache=False,
        enable_reranking=False
    )

    return HybridSearchService(
        config=config,
        embedding_provider=mock_embedding_provider,
        vector_store=mock_vector_store,
        keyword_store=mock_keyword_store
    )

class TestHybridSearchService:
    """Integration tests for hybrid search service."""

    @pytest.mark.asyncio
    async def test_search_basic(self, search_service):
        """Test basic search functionality."""
        results, metrics = await search_service.search("test query")

        assert len(results) > 0
        assert metrics.total_ms > 0
        assert not metrics.cache_hit

    @pytest.mark.asyncio
    async def test_search_with_filters(self, search_service, mock_vector_store, mock_keyword_store):
        """Test search with filters."""
        filters = {"source": "docs"}

        results, _ = await search_service.search("test query", filters=filters)

        # Verify filters were passed to stores
        mock_vector_store.search.assert_called_once()
        mock_keyword_store.search.assert_called_once()

        call_args = mock_vector_store.search.call_args
        assert call_args[1].get("filters") == filters or call_args[0][2] == filters

    @pytest.mark.asyncio
    async def test_search_combines_results(self, search_service):
        """Test that results from both stores are combined."""
        results, _ = await search_service.search("test query")

        # Should have results from both stores
        result_ids = {r["id"] for r in results}
        assert "1" in result_ids  # From vector only
        assert "2" in result_ids  # From both
        assert "3" in result_ids  # From keyword only

    @pytest.mark.asyncio
    async def test_search_metrics(self, search_service):
        """Test that metrics are properly collected."""
        _, metrics = await search_service.search("test query")

        assert metrics.vector_ms >= 0
        assert metrics.keyword_ms >= 0
        assert metrics.fusion_ms >= 0
        assert metrics.vector_count == 2
        assert metrics.keyword_count == 2

    @pytest.mark.asyncio
    async def test_parallel_execution(self, search_service, mock_vector_store, mock_keyword_store):
        """Test that vector and keyword search run in parallel."""
        # Add delay to mock stores
        async def delayed_vector_search(*args, **kwargs):
            await asyncio.sleep(0.1)
            return [{"id": "1", "content": "test", "score": 0.9}]

        async def delayed_keyword_search(*args, **kwargs):
            await asyncio.sleep(0.1)
            return [{"id": "2", "content": "test", "score": 10.0}]

        mock_vector_store.search = delayed_vector_search
        mock_keyword_store.search = delayed_keyword_search

        _, metrics = await search_service.search("test query")

        # Total time should be ~100ms, not ~200ms
        assert metrics.total_ms < 200
```

### Performance Tests

```python
# tests/test_performance.py

import pytest
import asyncio
import time
import statistics

@pytest.fixture
def performance_config():
    """Configuration for performance tests."""
    return {
        "iterations": 100,
        "warmup_iterations": 10,
        "latency_p95_threshold_ms": 200,
        "latency_p99_threshold_ms": 500,
    }

class TestPerformance:
    """Performance tests for hybrid search."""

    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_search_latency(self, search_service, performance_config):
        """Test search latency meets SLO."""
        latencies = []

        # Warmup
        for _ in range(performance_config["warmup_iterations"]):
            await search_service.search("warmup query")

        # Measure
        for _ in range(performance_config["iterations"]):
            start = time.perf_counter()
            await search_service.search("test query for latency measurement")
            latencies.append((time.perf_counter() - start) * 1000)

        # Calculate percentiles
        latencies.sort()
        p50 = latencies[len(latencies) // 2]
        p95 = latencies[int(len(latencies) * 0.95)]
        p99 = latencies[int(len(latencies) * 0.99)]

        print(f"Latency p50: {p50:.2f}ms, p95: {p95:.2f}ms, p99: {p99:.2f}ms")

        assert p95 < performance_config["latency_p95_threshold_ms"]
        assert p99 < performance_config["latency_p99_threshold_ms"]

    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_concurrent_searches(self, search_service):
        """Test handling concurrent search requests."""
        async def single_search(query_id: int):
            start = time.perf_counter()
            results, _ = await search_service.search(f"concurrent query {query_id}")
            return time.perf_counter() - start

        # Run 50 concurrent searches
        tasks = [single_search(i) for i in range(50)]
        latencies = await asyncio.gather(*tasks)

        # All should complete
        assert len(latencies) == 50

        # Average latency shouldn't degrade significantly
        avg_latency = statistics.mean(latencies) * 1000
        assert avg_latency < 500  # 500ms average under load
```

---

## Monitoring Templates

### Prometheus Metrics

```python
# monitoring/metrics.py

from prometheus_client import Counter, Histogram, Gauge, Info
import time
from functools import wraps

# Counters
SEARCH_REQUESTS = Counter(
    'hybrid_search_requests_total',
    'Total number of search requests',
    ['status', 'fusion_method']
)

CACHE_HITS = Counter(
    'hybrid_search_cache_hits_total',
    'Total number of cache hits'
)

CACHE_MISSES = Counter(
    'hybrid_search_cache_misses_total',
    'Total number of cache misses'
)

# Histograms
SEARCH_LATENCY = Histogram(
    'hybrid_search_latency_seconds',
    'Search request latency in seconds',
    ['component'],  # total, vector, keyword, fusion, rerank
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)

RESULTS_COUNT = Histogram(
    'hybrid_search_results_count',
    'Number of results returned',
    buckets=[0, 1, 5, 10, 20, 50, 100]
)

# Gauges
ACTIVE_SEARCHES = Gauge(
    'hybrid_search_active_requests',
    'Number of currently active search requests'
)

INDEX_SIZE = Gauge(
    'hybrid_search_index_size',
    'Number of documents in the index',
    ['store']  # vector, keyword
)

# Info
BUILD_INFO = Info(
    'hybrid_search_build',
    'Build information'
)

def track_search_metrics(func):
    """Decorator to track search metrics."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        ACTIVE_SEARCHES.inc()
        start_time = time.perf_counter()

        try:
            results, metrics = await func(*args, **kwargs)

            # Record latencies
            SEARCH_LATENCY.labels(component='total').observe(metrics.total_ms / 1000)
            SEARCH_LATENCY.labels(component='vector').observe(metrics.vector_ms / 1000)
            SEARCH_LATENCY.labels(component='keyword').observe(metrics.keyword_ms / 1000)
            SEARCH_LATENCY.labels(component='fusion').observe(metrics.fusion_ms / 1000)

            if metrics.rerank_ms > 0:
                SEARCH_LATENCY.labels(component='rerank').observe(metrics.rerank_ms / 1000)

            # Record results count
            RESULTS_COUNT.observe(len(results))

            # Record cache stats
            if metrics.cache_hit:
                CACHE_HITS.inc()
            else:
                CACHE_MISSES.inc()

            # Record success
            SEARCH_REQUESTS.labels(status='success', fusion_method='rrf').inc()

            return results, metrics

        except Exception as e:
            SEARCH_REQUESTS.labels(status='error', fusion_method='unknown').inc()
            raise

        finally:
            ACTIVE_SEARCHES.dec()

    return wrapper
```

### Grafana Dashboard JSON

```json
{
  "dashboard": {
    "title": "Hybrid Search Metrics",
    "panels": [
      {
        "title": "Search Latency (p95)",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(hybrid_search_latency_seconds_bucket{component=\"total\"}[5m]))",
            "legendFormat": "p95 Total"
          },
          {
            "expr": "histogram_quantile(0.95, rate(hybrid_search_latency_seconds_bucket{component=\"vector\"}[5m]))",
            "legendFormat": "p95 Vector"
          },
          {
            "expr": "histogram_quantile(0.95, rate(hybrid_search_latency_seconds_bucket{component=\"keyword\"}[5m]))",
            "legendFormat": "p95 Keyword"
          }
        ]
      },
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(hybrid_search_requests_total{status=\"success\"}[5m])",
            "legendFormat": "Success"
          },
          {
            "expr": "rate(hybrid_search_requests_total{status=\"error\"}[5m])",
            "legendFormat": "Error"
          }
        ]
      },
      {
        "title": "Cache Hit Rate",
        "type": "gauge",
        "targets": [
          {
            "expr": "rate(hybrid_search_cache_hits_total[5m]) / (rate(hybrid_search_cache_hits_total[5m]) + rate(hybrid_search_cache_misses_total[5m]))"
          }
        ]
      },
      {
        "title": "Active Requests",
        "type": "stat",
        "targets": [
          {
            "expr": "hybrid_search_active_requests"
          }
        ]
      }
    ]
  }
}
```

---

## Deployment Templates

### Dockerfile

```dockerfile
# Dockerfile

FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Production image
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy wheels and install
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*

# Copy application
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000 9090

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Terraform Module

```hcl
# terraform/hybrid-search/main.tf

variable "environment" {
  type        = string
  description = "Environment name (dev, staging, prod)"
}

variable "region" {
  type        = string
  description = "AWS region"
  default     = "us-east-1"
}

# Qdrant on ECS
resource "aws_ecs_service" "qdrant" {
  name            = "qdrant-${var.environment}"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.qdrant.arn
  desired_count   = var.environment == "prod" ? 3 : 1

  load_balancer {
    target_group_arn = aws_lb_target_group.qdrant.arn
    container_name   = "qdrant"
    container_port   = 6333
  }
}

# Elasticsearch on OpenSearch
resource "aws_opensearch_domain" "search" {
  domain_name    = "hybrid-search-${var.environment}"
  engine_version = "OpenSearch_2.11"

  cluster_config {
    instance_type          = var.environment == "prod" ? "r6g.large.search" : "t3.small.search"
    instance_count         = var.environment == "prod" ? 3 : 1
    zone_awareness_enabled = var.environment == "prod"
  }

  ebs_options {
    ebs_enabled = true
    volume_size = var.environment == "prod" ? 100 : 20
    volume_type = "gp3"
  }
}

# ElastiCache Redis
resource "aws_elasticache_cluster" "cache" {
  cluster_id           = "hybrid-search-cache-${var.environment}"
  engine               = "redis"
  node_type            = var.environment == "prod" ? "cache.r6g.large" : "cache.t3.micro"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis7"
  port                 = 6379
}

# Hybrid Search Service on ECS
resource "aws_ecs_service" "hybrid_search" {
  name            = "hybrid-search-${var.environment}"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.hybrid_search.arn
  desired_count   = var.environment == "prod" ? 3 : 1

  load_balancer {
    target_group_arn = aws_lb_target_group.hybrid_search.arn
    container_name   = "hybrid-search"
    container_port   = 8000
  }
}

output "search_endpoint" {
  value = aws_lb.main.dns_name
}
```

---

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic V2](https://docs.pydantic.dev/latest/)
- [Prometheus Python Client](https://prometheus.github.io/client_python/)
- [Docker Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Kubernetes Deployment Patterns](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
