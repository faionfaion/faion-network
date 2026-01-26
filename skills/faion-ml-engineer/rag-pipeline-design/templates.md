# RAG Pipeline Templates

Production-ready templates for RAG system configurations.

---

## 1. Project Structure

```
rag-project/
├── src/
│   ├── __init__.py
│   ├── config.py           # Configuration management
│   ├── models.py           # Data models
│   ├── loaders/
│   │   ├── __init__.py
│   │   ├── base.py         # Loader interface
│   │   ├── pdf.py
│   │   ├── markdown.py
│   │   └── web.py
│   ├── chunking/
│   │   ├── __init__.py
│   │   ├── strategies.py
│   │   └── utils.py
│   ├── embedding/
│   │   ├── __init__.py
│   │   ├── service.py
│   │   └── cache.py
│   ├── retrieval/
│   │   ├── __init__.py
│   │   ├── vector_store.py
│   │   ├── reranker.py
│   │   └── hybrid.py
│   ├── generation/
│   │   ├── __init__.py
│   │   ├── llm.py
│   │   └── prompts.py
│   ├── pipeline.py         # Main RAG pipeline
│   └── api.py              # FastAPI endpoints
├── tests/
│   ├── test_loaders.py
│   ├── test_chunking.py
│   ├── test_retrieval.py
│   └── test_e2e.py
├── evaluation/
│   ├── datasets/           # Test question-answer pairs
│   ├── metrics.py
│   └── benchmark.py
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── config/
│   ├── default.yaml
│   ├── production.yaml
│   └── development.yaml
├── scripts/
│   ├── ingest.py
│   ├── evaluate.py
│   └── benchmark.py
├── pyproject.toml
└── README.md
```

---

## 2. Configuration Template

```yaml
# config/default.yaml
app:
  name: "RAG Service"
  version: "1.0.0"
  environment: "development"

embedding:
  provider: "openai"  # openai, voyageai, cohere, local
  model: "text-embedding-3-small"
  dimensions: 1536
  batch_size: 100
  cache:
    enabled: true
    backend: "redis"  # redis, memory
    ttl_seconds: 86400

chunking:
  strategy: "recursive"  # fixed, recursive, semantic, markdown
  chunk_size: 500
  chunk_overlap: 50
  min_chunk_size: 100

vector_store:
  provider: "qdrant"  # chroma, qdrant, pinecone, weaviate
  collection_name: "documents"

  # Qdrant-specific
  qdrant:
    url: "http://localhost:6333"
    api_key: null

  # Pinecone-specific
  pinecone:
    api_key: "${PINECONE_API_KEY}"
    environment: "us-east-1-aws"
    index_name: "rag-index"

  # Chroma-specific
  chroma:
    persist_directory: "./chroma_db"

retrieval:
  top_k: 5
  score_threshold: 0.5
  hybrid_search:
    enabled: true
    alpha: 0.5  # 0 = pure BM25, 1 = pure vector
  reranking:
    enabled: true
    model: "cross-encoder/ms-marco-MiniLM-L-6-v2"
    top_k_rerank: 20

generation:
  provider: "openai"  # openai, anthropic, local
  model: "gpt-4o"
  temperature: 0.2
  max_tokens: 1024
  streaming: true
  fallback_model: "gpt-4o-mini"

caching:
  query_cache:
    enabled: true
    ttl_seconds: 3600
  semantic_cache:
    enabled: true
    similarity_threshold: 0.95

monitoring:
  enabled: true
  provider: "prometheus"  # prometheus, datadog
  metrics_port: 9090
  tracing:
    enabled: true
    provider: "langsmith"  # langsmith, langfuse, jaeger

logging:
  level: "INFO"
  format: "json"
  include_query: true
  include_response: false  # Privacy consideration
```

---

## 3. Configuration Python Class

```python
# src/config.py
from pydantic import BaseSettings, Field
from typing import Optional, Literal
from pathlib import Path
import yaml

class EmbeddingConfig(BaseSettings):
    provider: Literal["openai", "voyageai", "cohere", "local"] = "openai"
    model: str = "text-embedding-3-small"
    dimensions: int = 1536
    batch_size: int = 100
    cache_enabled: bool = True
    cache_ttl: int = 86400

class ChunkingConfig(BaseSettings):
    strategy: Literal["fixed", "recursive", "semantic", "markdown"] = "recursive"
    chunk_size: int = 500
    chunk_overlap: int = 50
    min_chunk_size: int = 100

class VectorStoreConfig(BaseSettings):
    provider: Literal["chroma", "qdrant", "pinecone", "weaviate"] = "qdrant"
    collection_name: str = "documents"
    url: Optional[str] = "http://localhost:6333"
    api_key: Optional[str] = None

class RetrievalConfig(BaseSettings):
    top_k: int = 5
    score_threshold: float = 0.5
    hybrid_enabled: bool = True
    hybrid_alpha: float = 0.5
    rerank_enabled: bool = True
    rerank_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"

class GenerationConfig(BaseSettings):
    provider: Literal["openai", "anthropic", "local"] = "openai"
    model: str = "gpt-4o"
    temperature: float = 0.2
    max_tokens: int = 1024
    streaming: bool = True

class RAGConfig(BaseSettings):
    embedding: EmbeddingConfig = Field(default_factory=EmbeddingConfig)
    chunking: ChunkingConfig = Field(default_factory=ChunkingConfig)
    vector_store: VectorStoreConfig = Field(default_factory=VectorStoreConfig)
    retrieval: RetrievalConfig = Field(default_factory=RetrievalConfig)
    generation: GenerationConfig = Field(default_factory=GenerationConfig)

    @classmethod
    def from_yaml(cls, path: str) -> "RAGConfig":
        with open(path) as f:
            data = yaml.safe_load(f)
        return cls(**data)

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"
```

---

## 4. Docker Compose Template

```yaml
# docker/docker-compose.yml
version: "3.8"

services:
  rag-api:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - VECTOR_STORE__URL=http://qdrant:6333
      - REDIS_URL=redis://redis:6379
    depends_on:
      - qdrant
      - redis
    volumes:
      - ../data:/app/data
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_storage:/qdrant/storage
    environment:
      - QDRANT__SERVICE__GRPC_PORT=6334

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin

volumes:
  qdrant_storage:
  redis_data:
  prometheus_data:
  grafana_data:
```

---

## 5. Dockerfile Template

```dockerfile
# docker/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

# Copy application code
COPY src/ ./src/
COPY config/ ./config/

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 6. FastAPI Application Template

```python
# src/api.py
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import time

from src.config import RAGConfig
from src.pipeline import RAGPipeline
from src.models import Document

app = FastAPI(
    title="RAG API",
    description="Production RAG Pipeline API",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize pipeline
config = RAGConfig.from_yaml("config/default.yaml")
pipeline = RAGPipeline.from_config(config)


# Request/Response Models
class QueryRequest(BaseModel):
    question: str
    top_k: Optional[int] = 5
    filter: Optional[Dict] = None
    include_sources: bool = True

class QueryResponse(BaseModel):
    answer: str
    sources: Optional[List[Dict]] = None
    latency_ms: float

class IngestRequest(BaseModel):
    documents: List[Dict]  # {"content": str, "metadata": dict}

class IngestResponse(BaseModel):
    chunks_created: int
    documents_processed: int


# Endpoints
@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": time.time()}

@app.get("/ready")
async def ready():
    # Check dependencies
    try:
        # Quick vector store ping
        pipeline.vector_store.search(
            query_embedding=[0.0] * config.embedding.dimensions,
            top_k=1
        )
        return {"status": "ready"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Query the RAG pipeline."""
    try:
        result = pipeline.query(
            question=request.question,
            top_k=request.top_k,
            filter=request.filter
        )

        sources = None
        if request.include_sources:
            sources = [
                {
                    "content": r.chunk.content[:300],
                    "score": r.score,
                    "metadata": r.chunk.metadata
                }
                for r in result.sources
            ]

        return QueryResponse(
            answer=result.answer,
            sources=sources,
            latency_ms=result.latency_ms
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest", response_model=IngestResponse)
async def ingest(request: IngestRequest, background_tasks: BackgroundTasks):
    """Ingest documents into the pipeline."""
    documents = [
        Document(
            content=d["content"],
            metadata=d.get("metadata", {})
        )
        for d in request.documents
    ]

    # Ingest in background for large batches
    if len(documents) > 10:
        background_tasks.add_task(pipeline.ingest, documents)
        return IngestResponse(
            chunks_created=-1,  # Unknown, processing in background
            documents_processed=len(documents)
        )

    chunks_created = pipeline.ingest(documents)
    return IngestResponse(
        chunks_created=chunks_created,
        documents_processed=len(documents)
    )

@app.post("/retrieve")
async def retrieve(request: QueryRequest):
    """Retrieve relevant chunks without generation."""
    results = pipeline.retrieve(
        query=request.question,
        top_k=request.top_k,
        filter=request.filter
    )

    return {
        "results": [
            {
                "id": r.chunk.id,
                "content": r.chunk.content,
                "score": r.score,
                "metadata": r.chunk.metadata
            }
            for r in results
        ]
    }

@app.get("/stats")
async def stats():
    """Get pipeline statistics."""
    return {
        "total_documents": pipeline.get_document_count(),
        "total_chunks": pipeline.get_chunk_count(),
        "embedding_cache_size": pipeline.embedding_service.cache_info(),
    }
```

---

## 7. Evaluation Dataset Template

```yaml
# evaluation/datasets/qa_pairs.yaml
dataset_name: "RAG Evaluation Set v1"
created_at: "2025-01-01"
domain: "Technical Documentation"

questions:
  - id: "q001"
    question: "What is the system architecture?"
    expected_answer: "The system uses a microservices architecture with..."
    expected_sources:
      - "architecture.md"
    difficulty: "easy"
    category: "architecture"

  - id: "q002"
    question: "How do I configure authentication?"
    expected_answer: "Authentication is configured by setting..."
    expected_sources:
      - "auth-guide.md"
      - "config.md"
    difficulty: "medium"
    category: "configuration"

  - id: "q003"
    question: "What are the performance benchmarks?"
    expected_answer: "Performance benchmarks show..."
    expected_sources:
      - "benchmarks.md"
    difficulty: "easy"
    category: "performance"

# Questions that should return "I don't know"
negative_questions:
  - id: "neg001"
    question: "What is the weather today?"
    expected_behavior: "should_not_answer"

  - id: "neg002"
    question: "Write me a poem about cats"
    expected_behavior: "should_not_answer"
```

---

## 8. Prometheus Metrics Template

```python
# src/metrics.py
from prometheus_client import Counter, Histogram, Gauge, Info

# Request metrics
QUERY_COUNT = Counter(
    "rag_query_total",
    "Total number of RAG queries",
    ["status"]
)

QUERY_LATENCY = Histogram(
    "rag_query_latency_seconds",
    "RAG query latency",
    ["stage"],  # retrieval, generation, total
    buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

# Retrieval metrics
RETRIEVAL_RESULTS = Histogram(
    "rag_retrieval_results_count",
    "Number of results returned by retrieval",
    buckets=[0, 1, 3, 5, 10, 20]
)

RETRIEVAL_SCORE = Histogram(
    "rag_retrieval_top_score",
    "Top retrieval score",
    buckets=[0.1, 0.3, 0.5, 0.7, 0.8, 0.9, 0.95, 1.0]
)

# Token usage
TOKEN_USAGE = Counter(
    "rag_token_usage_total",
    "Total tokens used",
    ["type"]  # input, output
)

# Cache metrics
CACHE_HITS = Counter(
    "rag_cache_hits_total",
    "Total cache hits",
    ["cache_type"]  # embedding, query, semantic
)

CACHE_MISSES = Counter(
    "rag_cache_misses_total",
    "Total cache misses",
    ["cache_type"]
)

# Index metrics
INDEX_SIZE = Gauge(
    "rag_index_size_chunks",
    "Total chunks in vector index"
)

# System info
SYSTEM_INFO = Info(
    "rag_system",
    "RAG system information"
)

def record_query(latency: float, status: str, stage: str):
    QUERY_COUNT.labels(status=status).inc()
    QUERY_LATENCY.labels(stage=stage).observe(latency)

def record_retrieval(count: int, top_score: float):
    RETRIEVAL_RESULTS.observe(count)
    RETRIEVAL_SCORE.observe(top_score)

def record_tokens(input_tokens: int, output_tokens: int):
    TOKEN_USAGE.labels(type="input").inc(input_tokens)
    TOKEN_USAGE.labels(type="output").inc(output_tokens)

def record_cache(cache_type: str, hit: bool):
    if hit:
        CACHE_HITS.labels(cache_type=cache_type).inc()
    else:
        CACHE_MISSES.labels(cache_type=cache_type).inc()
```

---

## 9. Grafana Dashboard JSON Template

```json
{
  "title": "RAG Pipeline Dashboard",
  "panels": [
    {
      "title": "Query Rate",
      "type": "graph",
      "targets": [
        {
          "expr": "rate(rag_query_total[5m])",
          "legendFormat": "{{status}}"
        }
      ]
    },
    {
      "title": "Query Latency (p50, p95, p99)",
      "type": "graph",
      "targets": [
        {
          "expr": "histogram_quantile(0.5, rate(rag_query_latency_seconds_bucket{stage=\"total\"}[5m]))",
          "legendFormat": "p50"
        },
        {
          "expr": "histogram_quantile(0.95, rate(rag_query_latency_seconds_bucket{stage=\"total\"}[5m]))",
          "legendFormat": "p95"
        },
        {
          "expr": "histogram_quantile(0.99, rate(rag_query_latency_seconds_bucket{stage=\"total\"}[5m]))",
          "legendFormat": "p99"
        }
      ]
    },
    {
      "title": "Cache Hit Rate",
      "type": "gauge",
      "targets": [
        {
          "expr": "sum(rate(rag_cache_hits_total[5m])) / (sum(rate(rag_cache_hits_total[5m])) + sum(rate(rag_cache_misses_total[5m])))"
        }
      ]
    },
    {
      "title": "Token Usage",
      "type": "graph",
      "targets": [
        {
          "expr": "rate(rag_token_usage_total[5m])",
          "legendFormat": "{{type}}"
        }
      ]
    },
    {
      "title": "Retrieval Quality",
      "type": "graph",
      "targets": [
        {
          "expr": "histogram_quantile(0.5, rate(rag_retrieval_top_score_bucket[5m]))",
          "legendFormat": "Median Top Score"
        }
      ]
    },
    {
      "title": "Index Size",
      "type": "stat",
      "targets": [
        {
          "expr": "rag_index_size_chunks"
        }
      ]
    }
  ]
}
```

---

## 10. pyproject.toml Template

```toml
[tool.poetry]
name = "rag-pipeline"
version = "1.0.0"
description = "Production RAG Pipeline"
authors = ["Your Name <you@example.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.109.0"
uvicorn = {extras = ["standard"], version = "^0.27.0"}
openai = "^1.10.0"
anthropic = "^0.18.0"
qdrant-client = "^1.7.0"
chromadb = "^0.4.22"
pypdf = "^4.0.0"
pydantic = "^2.5.0"
pydantic-settings = "^2.1.0"
redis = "^5.0.0"
prometheus-client = "^0.19.0"
python-dotenv = "^1.0.0"
numpy = "^1.26.0"
nltk = "^3.8.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
pytest-asyncio = "^0.23.0"
pytest-cov = "^4.1.0"
httpx = "^0.26.0"
black = "^24.1.0"
ruff = "^0.1.0"
mypy = "^1.8.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.black]
line-length = 100
target-version = ["py311"]

[tool.ruff]
line-length = 100
select = ["E", "F", "I", "N", "W"]

[tool.mypy]
python_version = "3.11"
strict = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```
