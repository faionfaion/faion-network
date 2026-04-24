# Reranking Templates

Production-ready templates for reranking pipelines, configurations, and testing.

---

## Table of Contents

- [Pipeline Templates](#pipeline-templates)
- [Configuration Templates](#configuration-templates)
- [Service Templates](#service-templates)
- [Testing Templates](#testing-templates)
- [Monitoring Templates](#monitoring-templates)

---

## Pipeline Templates

### Basic Reranking Pipeline

```python
"""
Template: Basic two-stage retrieval pipeline with reranking.
Copy and customize for your use case.
"""
from typing import List, Dict, Any, Optional, Protocol
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# Configuration
# ============================================================================

@dataclass
class RerankerConfig:
    """Reranker configuration."""
    model_type: str = "cross-encoder"  # cross-encoder, cohere, jina, llm
    model_name: str = "cross-encoder/ms-marco-MiniLM-L-12-v2"
    api_key: Optional[str] = None
    device: str = "cpu"
    max_length: int = 512
    batch_size: int = 32
    timeout: int = 30


@dataclass
class RetrievalConfig:
    """Retrieval pipeline configuration."""
    initial_top_k: int = 50
    rerank_top_k: int = 5
    enable_reranking: bool = True
    fallback_on_error: bool = True
    cache_enabled: bool = True
    cache_ttl: int = 3600


# ============================================================================
# Interfaces
# ============================================================================

class Retriever(Protocol):
    """Interface for first-stage retriever."""
    def retrieve(self, query: str, top_k: int) -> List[Dict[str, Any]]: ...


class Reranker(Protocol):
    """Interface for reranker."""
    def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int
    ) -> List[Dict[str, Any]]: ...


# ============================================================================
# Reranker Factory
# ============================================================================

class RerankerFactory:
    """Factory for creating rerankers based on config."""

    @staticmethod
    def create(config: RerankerConfig) -> Reranker:
        """Create reranker from config."""
        if config.model_type == "cross-encoder":
            return CrossEncoderReranker(config)
        elif config.model_type == "cohere":
            return CohereReranker(config)
        elif config.model_type == "jina":
            return JinaReranker(config)
        elif config.model_type == "llm":
            return LLMReranker(config)
        else:
            raise ValueError(f"Unknown reranker type: {config.model_type}")


class CrossEncoderReranker:
    """Cross-encoder reranker implementation."""

    def __init__(self, config: RerankerConfig):
        from sentence_transformers import CrossEncoder
        self.model = CrossEncoder(config.model_name, device=config.device)
        self.batch_size = config.batch_size

    def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int
    ) -> List[Dict[str, Any]]:
        import numpy as np

        pairs = [[query, doc] for doc in documents]
        scores = self.model.predict(pairs, batch_size=self.batch_size)
        sorted_indices = np.argsort(scores)[::-1][:top_k]

        return [
            {
                "document": documents[i],
                "score": float(scores[i]),
                "original_index": int(i)
            }
            for i in sorted_indices
        ]


class CohereReranker:
    """Cohere API reranker implementation."""

    def __init__(self, config: RerankerConfig):
        import cohere
        self.client = cohere.Client(api_key=config.api_key, timeout=config.timeout)
        self.model = config.model_name or "rerank-english-v3.0"

    def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int
    ) -> List[Dict[str, Any]]:
        response = self.client.rerank(
            query=query,
            documents=documents,
            top_n=top_k,
            model=self.model
        )

        return [
            {
                "document": documents[r.index],
                "score": r.relevance_score,
                "original_index": r.index
            }
            for r in response.results
        ]


class JinaReranker:
    """Jina API reranker implementation."""

    def __init__(self, config: RerankerConfig):
        import httpx
        self.api_key = config.api_key
        self.model = config.model_name or "jina-reranker-v2-base-multilingual"
        self.timeout = config.timeout

    def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int
    ) -> List[Dict[str, Any]]:
        import httpx

        response = httpx.post(
            "https://api.jina.ai/v1/rerank",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "model": self.model,
                "query": query,
                "documents": documents,
                "top_n": top_k
            },
            timeout=self.timeout
        )
        response.raise_for_status()
        data = response.json()

        return [
            {
                "document": documents[r["index"]],
                "score": r["relevance_score"],
                "original_index": r["index"]
            }
            for r in data["results"]
        ]


class LLMReranker:
    """LLM-based reranker implementation."""

    def __init__(self, config: RerankerConfig):
        from openai import OpenAI
        self.client = OpenAI(api_key=config.api_key)
        self.model = config.model_name or "gpt-4o-mini"

    def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int
    ) -> List[Dict[str, Any]]:
        import json

        docs_text = "\n".join([f"[{i}] {doc[:300]}" for i, doc in enumerate(documents)])

        prompt = f"""Rank these documents by relevance to the query. Return JSON.

Query: {query}

Documents:
{docs_text}

Return: {{"rankings": [{{"index": 0, "score": 9.5}}, ...]}}
Top {top_k} only, sorted by score descending."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            response_format={"type": "json_object"}
        )

        result = json.loads(response.choices[0].message.content)

        return [
            {
                "document": documents[r["index"]],
                "score": r["score"],
                "original_index": r["index"]
            }
            for r in result["rankings"][:top_k]
        ]


# ============================================================================
# Main Pipeline
# ============================================================================

class RerankingPipeline:
    """
    Two-stage retrieval pipeline with reranking.

    Usage:
        config = RetrievalConfig(initial_top_k=50, rerank_top_k=5)
        reranker_config = RerankerConfig(model_type="cross-encoder")

        pipeline = RerankingPipeline(
            retriever=your_retriever,
            reranker_config=reranker_config,
            config=config
        )

        results = pipeline.retrieve("your query")
    """

    def __init__(
        self,
        retriever: Retriever,
        reranker_config: RerankerConfig,
        config: RetrievalConfig = None
    ):
        self.retriever = retriever
        self.config = config or RetrievalConfig()
        self.reranker = RerankerFactory.create(reranker_config)
        self._cache: Dict[str, Any] = {}

    def retrieve(
        self,
        query: str,
        filter: Optional[Dict] = None
    ) -> List[Dict[str, Any]]:
        """
        Execute two-stage retrieval with reranking.
        """
        try:
            # Check cache
            if self.config.cache_enabled:
                cache_key = f"{query}:{filter}"
                if cache_key in self._cache:
                    return self._cache[cache_key]

            # Stage 1: Initial retrieval
            initial_results = self.retriever.retrieve(
                query=query,
                top_k=self.config.initial_top_k
            )

            if not initial_results:
                return []

            # Stage 2: Reranking (if enabled)
            if self.config.enable_reranking:
                documents = [r.get("content", r.get("text", "")) for r in initial_results]

                reranked = self.reranker.rerank(
                    query=query,
                    documents=documents,
                    top_k=self.config.rerank_top_k
                )

                # Merge rerank scores with original metadata
                results = []
                for r in reranked:
                    original = initial_results[r["original_index"]].copy()
                    original["rerank_score"] = r["score"]
                    results.append(original)
            else:
                results = initial_results[:self.config.rerank_top_k]

            # Cache results
            if self.config.cache_enabled:
                self._cache[cache_key] = results

            return results

        except Exception as e:
            logger.error(f"Reranking failed: {e}")
            if self.config.fallback_on_error:
                return initial_results[:self.config.rerank_top_k]
            raise


# ============================================================================
# Usage Example
# ============================================================================

if __name__ == "__main__":
    # Example retriever (replace with your implementation)
    class MockRetriever:
        def __init__(self, documents: List[Dict]):
            self.documents = documents

        def retrieve(self, query: str, top_k: int) -> List[Dict]:
            # Simple mock - return first top_k docs
            return self.documents[:top_k]

    # Sample documents
    docs = [
        {"content": "Python is a programming language.", "id": 1},
        {"content": "Machine learning uses Python.", "id": 2},
        {"content": "JavaScript runs in browsers.", "id": 3},
        {"content": "Deep learning is part of ML.", "id": 4},
        {"content": "React is a JS framework.", "id": 5},
    ]

    # Create pipeline
    pipeline = RerankingPipeline(
        retriever=MockRetriever(docs),
        reranker_config=RerankerConfig(
            model_type="cross-encoder",
            model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"
        ),
        config=RetrievalConfig(initial_top_k=5, rerank_top_k=3)
    )

    # Query
    results = pipeline.retrieve("What is machine learning?")
    for r in results:
        print(f"[{r.get('rerank_score', 0):.3f}] {r['content']}")
```

### Hybrid Search Pipeline Template

```python
"""
Template: Hybrid search (BM25 + Dense) with RRF fusion and reranking.
"""
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import numpy as np


@dataclass
class HybridConfig:
    """Hybrid search configuration."""
    bm25_weight: float = 0.5
    dense_weight: float = 0.5
    rrf_k: int = 60
    initial_top_k: int = 100
    fusion_top_k: int = 50
    rerank_top_k: int = 5


def reciprocal_rank_fusion(
    rankings: List[List[Tuple[str, float]]],
    k: int = 60
) -> List[Tuple[str, float]]:
    """
    RRF fusion for multiple rankings.

    Args:
        rankings: List of (doc_id, score) rankings
        k: RRF constant

    Returns:
        Fused ranking
    """
    scores: Dict[str, float] = {}

    for ranking in rankings:
        for rank, (doc_id, _) in enumerate(ranking):
            if doc_id not in scores:
                scores[doc_id] = 0
            scores[doc_id] += 1 / (k + rank + 1)

    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


class HybridRerankingPipeline:
    """
    Hybrid search pipeline with:
    1. BM25 (sparse) retrieval
    2. Dense (vector) retrieval
    3. RRF fusion
    4. Cross-encoder reranking
    """

    def __init__(
        self,
        bm25_retriever,
        dense_retriever,
        reranker,
        document_store: Dict[str, str],  # doc_id -> content mapping
        config: HybridConfig = None
    ):
        self.bm25 = bm25_retriever
        self.dense = dense_retriever
        self.reranker = reranker
        self.document_store = document_store
        self.config = config or HybridConfig()

    def retrieve(self, query: str) -> List[Dict[str, Any]]:
        """Execute hybrid retrieval with reranking."""

        # Stage 1a: BM25 retrieval
        bm25_results = self.bm25.search(query, top_k=self.config.initial_top_k)
        bm25_ranking = [(r["id"], r["score"]) for r in bm25_results]

        # Stage 1b: Dense retrieval
        dense_results = self.dense.search(query, top_k=self.config.initial_top_k)
        dense_ranking = [(r["id"], r["score"]) for r in dense_results]

        # Stage 2: RRF fusion
        fused = reciprocal_rank_fusion(
            [bm25_ranking, dense_ranking],
            k=self.config.rrf_k
        )

        # Get documents for reranking
        fusion_ids = [doc_id for doc_id, _ in fused[:self.config.fusion_top_k]]
        fusion_docs = [self.document_store[doc_id] for doc_id in fusion_ids]

        # Stage 3: Reranking
        reranked = self.reranker.rerank(
            query=query,
            documents=fusion_docs,
            top_k=self.config.rerank_top_k
        )

        # Build final results
        results = []
        for r in reranked:
            doc_id = fusion_ids[r["original_index"]]
            results.append({
                "id": doc_id,
                "content": self.document_store[doc_id],
                "rerank_score": r["score"],
                "rrf_score": dict(fused)[doc_id]
            })

        return results
```

### Async Pipeline Template

```python
"""
Template: Async reranking pipeline for high-throughput applications.
"""
import asyncio
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import httpx


@dataclass
class AsyncConfig:
    api_url: str
    api_key: str
    model: str = "rerank-english-v3.0"
    max_concurrent: int = 10
    timeout: int = 30
    retry_attempts: int = 3


class AsyncRerankingPipeline:
    """
    Async reranking pipeline for high-throughput scenarios.
    """

    def __init__(
        self,
        retriever,  # Async retriever
        config: AsyncConfig
    ):
        self.retriever = retriever
        self.config = config
        self.semaphore = asyncio.Semaphore(config.max_concurrent)

    async def _rerank_with_retry(
        self,
        client: httpx.AsyncClient,
        query: str,
        documents: List[str],
        top_k: int
    ) -> List[Dict]:
        """Rerank with retry logic."""
        for attempt in range(self.config.retry_attempts):
            try:
                async with self.semaphore:
                    response = await client.post(
                        self.config.api_url,
                        json={
                            "query": query,
                            "documents": documents,
                            "top_n": top_k,
                            "model": self.config.model
                        },
                        headers={"Authorization": f"Bearer {self.config.api_key}"},
                        timeout=self.config.timeout
                    )
                    response.raise_for_status()
                    return response.json()["results"]
            except Exception as e:
                if attempt == self.config.retry_attempts - 1:
                    raise
                await asyncio.sleep(2 ** attempt)

    async def retrieve(
        self,
        query: str,
        initial_top_k: int = 50,
        rerank_top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Async retrieval with reranking."""
        # Stage 1: Async retrieval
        initial_results = await self.retriever.aretrieve(query, top_k=initial_top_k)

        if not initial_results:
            return []

        documents = [r["content"] for r in initial_results]

        # Stage 2: Async reranking
        async with httpx.AsyncClient() as client:
            reranked = await self._rerank_with_retry(
                client, query, documents, rerank_top_k
            )

        # Merge results
        results = []
        for r in reranked:
            original = initial_results[r["index"]].copy()
            original["rerank_score"] = r["relevance_score"]
            results.append(original)

        return results

    async def retrieve_batch(
        self,
        queries: List[str],
        initial_top_k: int = 50,
        rerank_top_k: int = 5
    ) -> List[List[Dict[str, Any]]]:
        """Batch async retrieval."""
        tasks = [
            self.retrieve(q, initial_top_k, rerank_top_k)
            for q in queries
        ]
        return await asyncio.gather(*tasks, return_exceptions=True)
```

---

## Configuration Templates

### YAML Configuration

```yaml
# reranking-config.yaml
# Production configuration for reranking pipeline

reranker:
  # Type: cross-encoder, cohere, jina, llm
  type: cross-encoder

  # Model configuration
  model:
    name: BAAI/bge-reranker-v2-m3
    device: cuda  # cuda, cpu, mps
    max_length: 512
    batch_size: 32

  # API configuration (for cohere, jina)
  api:
    key: ${RERANKER_API_KEY}  # Environment variable
    timeout: 30
    max_retries: 3

retrieval:
  # First stage retrieval
  initial_top_k: 50

  # After reranking
  rerank_top_k: 5

  # Enable/disable reranking
  enabled: true

  # Fallback to initial results on error
  fallback_on_error: true

performance:
  # Caching
  cache:
    enabled: true
    ttl_seconds: 3600
    max_size: 10000

  # Batching
  batch:
    max_batch_size: 100
    batch_timeout_ms: 50

  # Concurrency
  max_concurrent_requests: 10

monitoring:
  # Metrics
  metrics:
    enabled: true
    prefix: reranker

  # Logging
  logging:
    level: INFO
    format: json

  # Alerting thresholds
  alerts:
    latency_p99_ms: 500
    error_rate_percent: 1.0
```

### Python Configuration Loader

```python
"""
Template: Configuration loader for reranking pipeline.
"""
import os
import yaml
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from pathlib import Path


@dataclass
class ModelConfig:
    name: str = "cross-encoder/ms-marco-MiniLM-L-12-v2"
    device: str = "cpu"
    max_length: int = 512
    batch_size: int = 32


@dataclass
class APIConfig:
    key: Optional[str] = None
    timeout: int = 30
    max_retries: int = 3


@dataclass
class RerankerTypeConfig:
    type: str = "cross-encoder"
    model: ModelConfig = field(default_factory=ModelConfig)
    api: APIConfig = field(default_factory=APIConfig)


@dataclass
class RetrievalTypeConfig:
    initial_top_k: int = 50
    rerank_top_k: int = 5
    enabled: bool = True
    fallback_on_error: bool = True


@dataclass
class CacheConfig:
    enabled: bool = True
    ttl_seconds: int = 3600
    max_size: int = 10000


@dataclass
class BatchConfig:
    max_batch_size: int = 100
    batch_timeout_ms: int = 50


@dataclass
class PerformanceConfig:
    cache: CacheConfig = field(default_factory=CacheConfig)
    batch: BatchConfig = field(default_factory=BatchConfig)
    max_concurrent_requests: int = 10


@dataclass
class MetricsConfig:
    enabled: bool = True
    prefix: str = "reranker"


@dataclass
class LoggingConfig:
    level: str = "INFO"
    format: str = "json"


@dataclass
class AlertsConfig:
    latency_p99_ms: int = 500
    error_rate_percent: float = 1.0


@dataclass
class MonitoringConfig:
    metrics: MetricsConfig = field(default_factory=MetricsConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    alerts: AlertsConfig = field(default_factory=AlertsConfig)


@dataclass
class RerankingConfig:
    """Complete reranking configuration."""
    reranker: RerankerTypeConfig = field(default_factory=RerankerTypeConfig)
    retrieval: RetrievalTypeConfig = field(default_factory=RetrievalTypeConfig)
    performance: PerformanceConfig = field(default_factory=PerformanceConfig)
    monitoring: MonitoringConfig = field(default_factory=MonitoringConfig)

    @classmethod
    def from_yaml(cls, path: str) -> "RerankingConfig":
        """Load configuration from YAML file."""
        with open(path) as f:
            data = yaml.safe_load(f)

        # Expand environment variables
        data = cls._expand_env_vars(data)

        return cls._from_dict(data)

    @classmethod
    def _expand_env_vars(cls, data: Any) -> Any:
        """Recursively expand environment variables."""
        if isinstance(data, str):
            if data.startswith("${") and data.endswith("}"):
                env_var = data[2:-1]
                return os.environ.get(env_var, "")
            return data
        elif isinstance(data, dict):
            return {k: cls._expand_env_vars(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [cls._expand_env_vars(item) for item in data]
        return data

    @classmethod
    def _from_dict(cls, data: Dict) -> "RerankingConfig":
        """Create config from dictionary."""
        reranker_data = data.get("reranker", {})
        retrieval_data = data.get("retrieval", {})
        performance_data = data.get("performance", {})
        monitoring_data = data.get("monitoring", {})

        return cls(
            reranker=RerankerTypeConfig(
                type=reranker_data.get("type", "cross-encoder"),
                model=ModelConfig(**reranker_data.get("model", {})),
                api=APIConfig(**reranker_data.get("api", {}))
            ),
            retrieval=RetrievalTypeConfig(**retrieval_data),
            performance=PerformanceConfig(
                cache=CacheConfig(**performance_data.get("cache", {})),
                batch=BatchConfig(**performance_data.get("batch", {})),
                max_concurrent_requests=performance_data.get("max_concurrent_requests", 10)
            ),
            monitoring=MonitoringConfig(
                metrics=MetricsConfig(**monitoring_data.get("metrics", {})),
                logging=LoggingConfig(**monitoring_data.get("logging", {})),
                alerts=AlertsConfig(**monitoring_data.get("alerts", {}))
            )
        )


# Usage
if __name__ == "__main__":
    # Load from file
    config = RerankingConfig.from_yaml("reranking-config.yaml")

    # Or create programmatically
    config = RerankingConfig(
        reranker=RerankerTypeConfig(
            type="cohere",
            api=APIConfig(key=os.getenv("COHERE_API_KEY"))
        ),
        retrieval=RetrievalTypeConfig(initial_top_k=100, rerank_top_k=10)
    )

    print(f"Reranker type: {config.reranker.type}")
    print(f"Initial top-k: {config.retrieval.initial_top_k}")
```

### Environment-Based Configuration

```python
"""
Template: Environment-based configuration with validation.
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, Literal
import os


class RerankerEnvConfig(BaseModel):
    """Reranker configuration from environment variables."""

    # Reranker type
    reranker_type: Literal["cross-encoder", "cohere", "jina", "llm"] = Field(
        default="cross-encoder",
        env="RERANKER_TYPE"
    )

    # Model settings
    model_name: str = Field(
        default="cross-encoder/ms-marco-MiniLM-L-12-v2",
        env="RERANKER_MODEL"
    )
    device: str = Field(default="cpu", env="RERANKER_DEVICE")
    max_length: int = Field(default=512, env="RERANKER_MAX_LENGTH")
    batch_size: int = Field(default=32, env="RERANKER_BATCH_SIZE")

    # API settings
    api_key: Optional[str] = Field(default=None, env="RERANKER_API_KEY")
    api_timeout: int = Field(default=30, env="RERANKER_API_TIMEOUT")

    # Retrieval settings
    initial_top_k: int = Field(default=50, env="RERANKER_INITIAL_TOP_K")
    rerank_top_k: int = Field(default=5, env="RERANKER_RERANK_TOP_K")

    # Performance
    cache_enabled: bool = Field(default=True, env="RERANKER_CACHE_ENABLED")
    cache_ttl: int = Field(default=3600, env="RERANKER_CACHE_TTL")
    max_concurrent: int = Field(default=10, env="RERANKER_MAX_CONCURRENT")

    class Config:
        env_prefix = ""  # Don't add prefix, we define each env explicitly

    @validator("api_key", always=True)
    def validate_api_key(cls, v, values):
        """Ensure API key is provided for API-based rerankers."""
        reranker_type = values.get("reranker_type")
        if reranker_type in ["cohere", "jina"] and not v:
            raise ValueError(f"API key required for {reranker_type} reranker")
        return v

    @validator("device")
    def validate_device(cls, v):
        """Validate device setting."""
        import torch
        valid_devices = ["cpu"]
        if torch.cuda.is_available():
            valid_devices.append("cuda")
        if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            valid_devices.append("mps")

        if v not in valid_devices:
            raise ValueError(f"Device {v} not available. Valid: {valid_devices}")
        return v

    @classmethod
    def from_env(cls) -> "RerankerEnvConfig":
        """Load configuration from environment variables."""
        return cls(
            reranker_type=os.getenv("RERANKER_TYPE", "cross-encoder"),
            model_name=os.getenv("RERANKER_MODEL", "cross-encoder/ms-marco-MiniLM-L-12-v2"),
            device=os.getenv("RERANKER_DEVICE", "cpu"),
            max_length=int(os.getenv("RERANKER_MAX_LENGTH", "512")),
            batch_size=int(os.getenv("RERANKER_BATCH_SIZE", "32")),
            api_key=os.getenv("RERANKER_API_KEY"),
            api_timeout=int(os.getenv("RERANKER_API_TIMEOUT", "30")),
            initial_top_k=int(os.getenv("RERANKER_INITIAL_TOP_K", "50")),
            rerank_top_k=int(os.getenv("RERANKER_RERANK_TOP_K", "5")),
            cache_enabled=os.getenv("RERANKER_CACHE_ENABLED", "true").lower() == "true",
            cache_ttl=int(os.getenv("RERANKER_CACHE_TTL", "3600")),
            max_concurrent=int(os.getenv("RERANKER_MAX_CONCURRENT", "10"))
        )


# Example .env file content:
"""
# .env
RERANKER_TYPE=cohere
RERANKER_MODEL=rerank-english-v3.0
RERANKER_API_KEY=your-api-key-here
RERANKER_INITIAL_TOP_K=100
RERANKER_RERANK_TOP_K=10
RERANKER_CACHE_ENABLED=true
"""
```

---

## Service Templates

### FastAPI Service Template

```python
"""
Template: FastAPI service for reranking.
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import logging
from contextlib import asynccontextmanager
import time

logger = logging.getLogger(__name__)


# ============================================================================
# Models
# ============================================================================

class Document(BaseModel):
    """Input document."""
    text: str
    id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class RerankRequest(BaseModel):
    """Rerank request."""
    query: str = Field(..., min_length=1, max_length=10000)
    documents: List[Document] = Field(..., min_items=1, max_items=1000)
    top_k: int = Field(default=5, ge=1, le=100)
    return_documents: bool = True


class RerankResult(BaseModel):
    """Single rerank result."""
    index: int
    score: float
    document: Optional[Document] = None


class RerankResponse(BaseModel):
    """Rerank response."""
    results: List[RerankResult]
    model: str
    latency_ms: float


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    model_loaded: bool
    version: str


# ============================================================================
# Service
# ============================================================================

class RerankingService:
    """Reranking service with health checks and metrics."""

    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-12-v2"):
        self.model_name = model_name
        self.reranker = None
        self._load_model()

    def _load_model(self):
        """Load the reranking model."""
        from sentence_transformers import CrossEncoder
        logger.info(f"Loading model: {self.model_name}")
        self.reranker = CrossEncoder(self.model_name)
        logger.info("Model loaded successfully")

    def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Rerank documents."""
        import numpy as np

        pairs = [[query, doc] for doc in documents]
        scores = self.reranker.predict(pairs)
        sorted_indices = np.argsort(scores)[::-1][:top_k]

        return [
            {
                "index": int(idx),
                "score": float(scores[idx])
            }
            for idx in sorted_indices
        ]

    @property
    def is_ready(self) -> bool:
        """Check if service is ready."""
        return self.reranker is not None


# ============================================================================
# FastAPI App
# ============================================================================

# Global service instance
service: Optional[RerankingService] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage service lifecycle."""
    global service
    service = RerankingService()
    yield
    service = None


app = FastAPI(
    title="Reranking Service",
    description="Cross-encoder reranking API",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy" if service and service.is_ready else "unhealthy",
        model_loaded=service.is_ready if service else False,
        version="1.0.0"
    )


@app.post("/rerank", response_model=RerankResponse)
async def rerank(request: RerankRequest):
    """Rerank documents by relevance to query."""
    if not service or not service.is_ready:
        raise HTTPException(status_code=503, detail="Service not ready")

    start_time = time.time()

    try:
        documents = [doc.text for doc in request.documents]

        results = service.rerank(
            query=request.query,
            documents=documents,
            top_k=request.top_k
        )

        # Build response
        response_results = []
        for r in results:
            result = RerankResult(
                index=r["index"],
                score=r["score"],
                document=request.documents[r["index"]] if request.return_documents else None
            )
            response_results.append(result)

        latency_ms = (time.time() - start_time) * 1000

        return RerankResponse(
            results=response_results,
            model=service.model_name,
            latency_ms=latency_ms
        )

    except Exception as e:
        logger.error(f"Reranking failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Run with: uvicorn reranking_service:app --host 0.0.0.0 --port 8000
```

### Docker Template

```dockerfile
# Dockerfile for reranking service
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Download model at build time (optional)
RUN python -c "from sentence_transformers import CrossEncoder; CrossEncoder('cross-encoder/ms-marco-MiniLM-L-12-v2')"

# Run service
EXPOSE 8000
CMD ["uvicorn", "reranking_service:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yaml
version: '3.8'

services:
  reranker:
    build: .
    ports:
      - "8000:8000"
    environment:
      - RERANKER_MODEL=cross-encoder/ms-marco-MiniLM-L-12-v2
      - RERANKER_DEVICE=cpu
    volumes:
      - model-cache:/root/.cache
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          memory: 4G
        reservations:
          memory: 2G

volumes:
  model-cache:
```

---

## Testing Templates

### Unit Test Template

```python
"""
Template: Unit tests for reranking components.
"""
import pytest
from unittest.mock import Mock, patch
import numpy as np


class TestRerankerUnit:
    """Unit tests for reranker class."""

    @pytest.fixture
    def mock_cross_encoder(self):
        """Mock CrossEncoder model."""
        mock = Mock()
        mock.predict.return_value = np.array([0.9, 0.3, 0.7, 0.1, 0.5])
        return mock

    @pytest.fixture
    def reranker(self, mock_cross_encoder):
        """Create reranker with mocked model."""
        with patch("sentence_transformers.CrossEncoder", return_value=mock_cross_encoder):
            from your_module import BasicReranker
            return BasicReranker(model_name="test-model")

    def test_rerank_returns_top_k(self, reranker):
        """Test that rerank returns exactly top_k results."""
        query = "test query"
        documents = ["doc1", "doc2", "doc3", "doc4", "doc5"]

        results = reranker.rerank(query, documents, top_k=3)

        assert len(results) == 3

    def test_rerank_sorted_by_score(self, reranker):
        """Test that results are sorted by score descending."""
        query = "test query"
        documents = ["doc1", "doc2", "doc3", "doc4", "doc5"]

        results = reranker.rerank(query, documents, top_k=5)

        scores = [r["score"] for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_rerank_empty_documents(self, reranker):
        """Test reranking with empty document list."""
        results = reranker.rerank("query", [], top_k=5)
        assert results == []

    def test_rerank_preserves_original_index(self, reranker):
        """Test that original indices are correctly preserved."""
        query = "test query"
        documents = ["doc1", "doc2", "doc3", "doc4", "doc5"]

        results = reranker.rerank(query, documents, top_k=5)

        # Highest score (0.9) is at index 0
        assert results[0]["original_index"] == 0
        # Second highest (0.7) is at index 2
        assert results[1]["original_index"] == 2

    def test_rerank_score_format(self, reranker):
        """Test that scores are float type."""
        query = "test query"
        documents = ["doc1", "doc2"]

        results = reranker.rerank(query, documents, top_k=2)

        for r in results:
            assert isinstance(r["score"], float)

    def test_rerank_top_k_larger_than_docs(self, reranker):
        """Test when top_k is larger than document count."""
        query = "test query"
        documents = ["doc1", "doc2"]

        results = reranker.rerank(query, documents, top_k=10)

        assert len(results) == 2


class TestRerankerIntegration:
    """Integration tests with real model (optional, slow)."""

    @pytest.fixture
    def real_reranker(self):
        """Create real reranker (requires model download)."""
        from your_module import BasicReranker
        return BasicReranker(model_name="cross-encoder/ms-marco-MiniLM-L-6-v2")

    @pytest.mark.slow
    def test_real_model_relevance(self, real_reranker):
        """Test that real model ranks relevant docs higher."""
        query = "What is the capital of France?"
        documents = [
            "Python is a programming language.",
            "Paris is the capital of France.",
            "The weather is nice today."
        ]

        results = real_reranker.rerank(query, documents, top_k=3)

        # Paris doc should be ranked first
        assert "Paris" in results[0]["document"]
```

### Benchmark Template

```python
"""
Template: Benchmark tests for reranking performance.
"""
import pytest
import time
import statistics
from typing import List, Dict
import json


class RerankingBenchmark:
    """Benchmark reranking performance."""

    def __init__(self, reranker):
        self.reranker = reranker
        self.results: List[Dict] = []

    def run_latency_benchmark(
        self,
        query: str,
        documents: List[str],
        iterations: int = 100,
        warmup: int = 10
    ) -> Dict:
        """Measure reranking latency."""
        # Warmup
        for _ in range(warmup):
            self.reranker.rerank(query, documents, top_k=5)

        # Benchmark
        latencies = []
        for _ in range(iterations):
            start = time.perf_counter()
            self.reranker.rerank(query, documents, top_k=5)
            latencies.append((time.perf_counter() - start) * 1000)  # ms

        result = {
            "iterations": iterations,
            "doc_count": len(documents),
            "p50_ms": statistics.median(latencies),
            "p90_ms": sorted(latencies)[int(iterations * 0.9)],
            "p99_ms": sorted(latencies)[int(iterations * 0.99)],
            "mean_ms": statistics.mean(latencies),
            "std_ms": statistics.stdev(latencies)
        }

        self.results.append(result)
        return result

    def run_throughput_benchmark(
        self,
        query: str,
        documents: List[str],
        duration_seconds: int = 10
    ) -> Dict:
        """Measure reranking throughput."""
        start = time.perf_counter()
        count = 0

        while time.perf_counter() - start < duration_seconds:
            self.reranker.rerank(query, documents, top_k=5)
            count += 1

        elapsed = time.perf_counter() - start

        result = {
            "duration_seconds": elapsed,
            "total_requests": count,
            "requests_per_second": count / elapsed,
            "doc_count": len(documents)
        }

        self.results.append(result)
        return result

    def save_results(self, path: str):
        """Save benchmark results to file."""
        with open(path, "w") as f:
            json.dump(self.results, f, indent=2)


# Pytest benchmarks
class TestRerankingBenchmarks:
    """Benchmark tests using pytest."""

    @pytest.fixture
    def reranker(self):
        from your_module import BasicReranker
        return BasicReranker(model_name="cross-encoder/ms-marco-MiniLM-L-6-v2")

    @pytest.fixture
    def sample_documents(self):
        return [f"This is sample document number {i}" for i in range(50)]

    @pytest.mark.benchmark
    def test_latency_50_docs(self, reranker, sample_documents, benchmark):
        """Benchmark latency for 50 documents."""
        result = benchmark(
            reranker.rerank,
            "test query",
            sample_documents,
            5
        )
        assert len(result) == 5

    @pytest.mark.benchmark
    def test_latency_100_docs(self, reranker, benchmark):
        """Benchmark latency for 100 documents."""
        docs = [f"Document {i}" for i in range(100)]
        result = benchmark(
            reranker.rerank,
            "test query",
            docs,
            5
        )
        assert len(result) == 5


# Run with: pytest benchmark_tests.py -v --benchmark-only
```

### Quality Evaluation Template

```python
"""
Template: Quality evaluation for reranking.
"""
from typing import List, Dict, Tuple
import numpy as np
from dataclasses import dataclass


@dataclass
class EvaluationResult:
    """Evaluation metrics result."""
    ndcg_at_k: Dict[int, float]
    mrr: float
    precision_at_k: Dict[int, float]
    recall_at_k: Dict[int, float]
    map_score: float


class RerankingEvaluator:
    """Evaluate reranking quality."""

    def __init__(self, reranker):
        self.reranker = reranker

    def evaluate(
        self,
        queries: List[str],
        documents_per_query: List[List[str]],
        relevance_labels: List[List[int]],  # 0/1 or graded relevance
        k_values: List[int] = [1, 3, 5, 10]
    ) -> EvaluationResult:
        """
        Evaluate reranking quality on a dataset.

        Args:
            queries: List of queries
            documents_per_query: Documents for each query
            relevance_labels: Relevance labels (same order as documents)
            k_values: K values for metrics

        Returns:
            Evaluation metrics
        """
        ndcg_scores = {k: [] for k in k_values}
        mrr_scores = []
        precision_scores = {k: [] for k in k_values}
        recall_scores = {k: [] for k in k_values}
        ap_scores = []

        for query, docs, labels in zip(queries, documents_per_query, relevance_labels):
            # Rerank
            results = self.reranker.rerank(query, docs, top_k=max(k_values))

            # Get reranked indices
            reranked_indices = [r["original_index"] for r in results]

            # Calculate metrics
            for k in k_values:
                ndcg_scores[k].append(
                    self._ndcg_at_k(labels, reranked_indices, k)
                )
                precision_scores[k].append(
                    self._precision_at_k(labels, reranked_indices, k)
                )
                recall_scores[k].append(
                    self._recall_at_k(labels, reranked_indices, k)
                )

            mrr_scores.append(self._mrr(labels, reranked_indices))
            ap_scores.append(self._average_precision(labels, reranked_indices))

        return EvaluationResult(
            ndcg_at_k={k: np.mean(scores) for k, scores in ndcg_scores.items()},
            mrr=np.mean(mrr_scores),
            precision_at_k={k: np.mean(scores) for k, scores in precision_scores.items()},
            recall_at_k={k: np.mean(scores) for k, scores in recall_scores.items()},
            map_score=np.mean(ap_scores)
        )

    def _ndcg_at_k(
        self,
        relevance: List[int],
        ranking: List[int],
        k: int
    ) -> float:
        """Calculate NDCG@k."""
        dcg = 0.0
        for i, idx in enumerate(ranking[:k]):
            rel = relevance[idx]
            dcg += (2 ** rel - 1) / np.log2(i + 2)

        # Ideal DCG
        sorted_rel = sorted(relevance, reverse=True)
        idcg = sum(
            (2 ** rel - 1) / np.log2(i + 2)
            for i, rel in enumerate(sorted_rel[:k])
        )

        return dcg / idcg if idcg > 0 else 0.0

    def _mrr(self, relevance: List[int], ranking: List[int]) -> float:
        """Calculate Mean Reciprocal Rank."""
        for i, idx in enumerate(ranking):
            if relevance[idx] > 0:
                return 1.0 / (i + 1)
        return 0.0

    def _precision_at_k(
        self,
        relevance: List[int],
        ranking: List[int],
        k: int
    ) -> float:
        """Calculate Precision@k."""
        relevant_in_top_k = sum(
            1 for idx in ranking[:k] if relevance[idx] > 0
        )
        return relevant_in_top_k / k

    def _recall_at_k(
        self,
        relevance: List[int],
        ranking: List[int],
        k: int
    ) -> float:
        """Calculate Recall@k."""
        total_relevant = sum(1 for r in relevance if r > 0)
        if total_relevant == 0:
            return 0.0

        relevant_in_top_k = sum(
            1 for idx in ranking[:k] if relevance[idx] > 0
        )
        return relevant_in_top_k / total_relevant

    def _average_precision(
        self,
        relevance: List[int],
        ranking: List[int]
    ) -> float:
        """Calculate Average Precision."""
        relevant_count = 0
        precision_sum = 0.0

        for i, idx in enumerate(ranking):
            if relevance[idx] > 0:
                relevant_count += 1
                precision_sum += relevant_count / (i + 1)

        total_relevant = sum(1 for r in relevance if r > 0)
        return precision_sum / total_relevant if total_relevant > 0 else 0.0


# Usage
if __name__ == "__main__":
    from your_module import BasicReranker

    reranker = BasicReranker()
    evaluator = RerankingEvaluator(reranker)

    # Sample evaluation data
    queries = ["machine learning", "python programming"]
    docs = [
        ["ML is AI subset", "Python is a language", "Deep learning uses ML"],
        ["Python syntax is clean", "Java is compiled", "Python for data science"]
    ]
    labels = [
        [1, 0, 1],  # First and third are relevant
        [1, 0, 1]   # First and third are relevant
    ]

    result = evaluator.evaluate(queries, docs, labels)

    print(f"NDCG@5: {result.ndcg_at_k[5]:.4f}")
    print(f"MRR: {result.mrr:.4f}")
    print(f"MAP: {result.map_score:.4f}")
```

---

## Monitoring Templates

### Prometheus Metrics Template

```python
"""
Template: Prometheus metrics for reranking service.
"""
from prometheus_client import Counter, Histogram, Gauge, Info
import time
from functools import wraps


# ============================================================================
# Metrics Definition
# ============================================================================

# Counters
RERANK_REQUESTS_TOTAL = Counter(
    "reranker_requests_total",
    "Total reranking requests",
    ["model", "status"]
)

RERANK_DOCUMENTS_TOTAL = Counter(
    "reranker_documents_total",
    "Total documents reranked",
    ["model"]
)

# Histograms
RERANK_LATENCY = Histogram(
    "reranker_latency_seconds",
    "Reranking latency in seconds",
    ["model"],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

RERANK_DOCUMENT_COUNT = Histogram(
    "reranker_document_count",
    "Number of documents per rerank request",
    ["model"],
    buckets=[1, 5, 10, 25, 50, 100, 250, 500, 1000]
)

RERANK_TOP_SCORE = Histogram(
    "reranker_top_score",
    "Top relevance score per request",
    ["model"],
    buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
)

# Gauges
RERANK_MODEL_LOADED = Gauge(
    "reranker_model_loaded",
    "Whether the model is loaded",
    ["model"]
)

RERANK_QUEUE_SIZE = Gauge(
    "reranker_queue_size",
    "Current request queue size"
)

# Info
RERANK_MODEL_INFO = Info(
    "reranker_model",
    "Information about the loaded model"
)


# ============================================================================
# Instrumented Reranker
# ============================================================================

class InstrumentedReranker:
    """Reranker with Prometheus metrics instrumentation."""

    def __init__(self, reranker, model_name: str):
        self.reranker = reranker
        self.model_name = model_name

        # Set model info
        RERANK_MODEL_INFO.info({
            "name": model_name,
            "type": type(reranker).__name__
        })
        RERANK_MODEL_LOADED.labels(model=model_name).set(1)

    def rerank(self, query: str, documents: list, top_k: int = 5) -> list:
        """Rerank with metrics collection."""
        doc_count = len(documents)
        RERANK_DOCUMENT_COUNT.labels(model=self.model_name).observe(doc_count)

        start_time = time.time()
        try:
            results = self.reranker.rerank(query, documents, top_k)

            # Record success metrics
            RERANK_REQUESTS_TOTAL.labels(
                model=self.model_name,
                status="success"
            ).inc()

            RERANK_DOCUMENTS_TOTAL.labels(
                model=self.model_name
            ).inc(doc_count)

            # Record top score
            if results:
                RERANK_TOP_SCORE.labels(
                    model=self.model_name
                ).observe(results[0].get("score", 0))

            return results

        except Exception as e:
            RERANK_REQUESTS_TOTAL.labels(
                model=self.model_name,
                status="error"
            ).inc()
            raise

        finally:
            latency = time.time() - start_time
            RERANK_LATENCY.labels(model=self.model_name).observe(latency)


# ============================================================================
# FastAPI Integration
# ============================================================================

def setup_metrics_endpoint(app):
    """Add /metrics endpoint to FastAPI app."""
    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
    from fastapi.responses import Response

    @app.get("/metrics")
    async def metrics():
        return Response(
            content=generate_latest(),
            media_type=CONTENT_TYPE_LATEST
        )
```

### Grafana Dashboard Template

```json
{
  "dashboard": {
    "title": "Reranking Service Dashboard",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(reranker_requests_total[5m])",
            "legendFormat": "{{model}} - {{status}}"
          }
        ]
      },
      {
        "title": "Latency P50/P90/P99",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.50, rate(reranker_latency_seconds_bucket[5m]))",
            "legendFormat": "p50"
          },
          {
            "expr": "histogram_quantile(0.90, rate(reranker_latency_seconds_bucket[5m]))",
            "legendFormat": "p90"
          },
          {
            "expr": "histogram_quantile(0.99, rate(reranker_latency_seconds_bucket[5m]))",
            "legendFormat": "p99"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(reranker_requests_total{status=\"error\"}[5m]) / rate(reranker_requests_total[5m]) * 100",
            "legendFormat": "Error %"
          }
        ]
      },
      {
        "title": "Documents per Request",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.50, rate(reranker_document_count_bucket[5m]))",
            "legendFormat": "Median docs/request"
          }
        ]
      },
      {
        "title": "Top Score Distribution",
        "type": "heatmap",
        "targets": [
          {
            "expr": "rate(reranker_top_score_bucket[5m])",
            "format": "heatmap"
          }
        ]
      }
    ]
  }
}
```

### Alerting Rules Template

```yaml
# alerting-rules.yaml
groups:
  - name: reranker_alerts
    rules:
      - alert: RerankerHighLatency
        expr: histogram_quantile(0.99, rate(reranker_latency_seconds_bucket[5m])) > 0.5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Reranker P99 latency is high"
          description: "P99 latency is {{ $value }}s, threshold is 0.5s"

      - alert: RerankerHighErrorRate
        expr: |
          rate(reranker_requests_total{status="error"}[5m])
          / rate(reranker_requests_total[5m]) > 0.01
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Reranker error rate is above 1%"
          description: "Error rate is {{ $value | humanizePercentage }}"

      - alert: RerankerDown
        expr: reranker_model_loaded == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Reranker model not loaded"
          description: "The reranking model is not loaded or service is down"

      - alert: RerankerLowThroughput
        expr: rate(reranker_requests_total[5m]) < 1
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Reranker throughput is unusually low"
          description: "Less than 1 request per second for 10 minutes"
```
