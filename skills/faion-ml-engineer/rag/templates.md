# RAG Templates

Ready-to-use templates for RAG pipelines, configurations, and prompts.

## Table of Contents

1. [Pipeline Templates](#pipeline-templates)
2. [Configuration Templates](#configuration-templates)
3. [Prompt Templates](#prompt-templates)
4. [Evaluation Templates](#evaluation-templates)
5. [Docker Deployment](#docker-deployment)

---

## Pipeline Templates

### Basic RAG Pipeline

```python
"""
Template: Basic RAG Pipeline
Use for: Simple Q&A applications, documentation search
"""
from dataclasses import dataclass
from typing import List, Optional
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI


@dataclass
class RAGConfig:
    """RAG pipeline configuration."""
    data_dir: str
    chunk_size: int = 1024
    chunk_overlap: int = 200
    embedding_model: str = "text-embedding-3-large"
    llm_model: str = "gpt-4o-mini"
    temperature: float = 0.0
    top_k: int = 5


class BasicRAGPipeline:
    """Basic RAG pipeline template."""

    def __init__(self, config: RAGConfig):
        self.config = config

        # Configure models
        Settings.embed_model = OpenAIEmbedding(model=config.embedding_model)
        Settings.llm = OpenAI(model=config.llm_model, temperature=config.temperature)

        self.index = None

    def build_index(self) -> int:
        """Build index from documents. Returns chunk count."""
        # Load documents
        documents = SimpleDirectoryReader(
            input_dir=self.config.data_dir,
            recursive=True,
        ).load_data()

        # Parse into chunks
        parser = SentenceSplitter(
            chunk_size=self.config.chunk_size,
            chunk_overlap=self.config.chunk_overlap,
        )
        nodes = parser.get_nodes_from_documents(documents)

        # Create index
        self.index = VectorStoreIndex(nodes, show_progress=True)

        return len(nodes)

    def query(self, question: str) -> dict:
        """Query the RAG system."""
        if not self.index:
            raise ValueError("Index not built. Call build_index() first.")

        query_engine = self.index.as_query_engine(
            similarity_top_k=self.config.top_k,
        )

        response = query_engine.query(question)

        return {
            "answer": response.response,
            "sources": [
                {
                    "file": node.metadata.get("file_name", "unknown"),
                    "score": node.score,
                }
                for node in response.source_nodes
            ]
        }


# Usage
if __name__ == "__main__":
    config = RAGConfig(data_dir="./data")
    pipeline = BasicRAGPipeline(config)
    chunk_count = pipeline.build_index()
    print(f"Indexed {chunk_count} chunks")

    result = pipeline.query("What is the main topic?")
    print(result["answer"])
```

### Production RAG Pipeline

```python
"""
Template: Production RAG Pipeline
Use for: Production applications with caching, monitoring, reranking
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging
import time
import uuid

from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.core.postprocessor import SentenceTransformerRerank
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from qdrant_client import QdrantClient
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ProductionConfig:
    """Production RAG configuration."""
    # Vector store
    qdrant_url: str = "localhost"
    qdrant_port: int = 6333
    collection_name: str = "production_kb"

    # Chunking
    chunk_size: int = 1024
    chunk_overlap: int = 200

    # Models
    embedding_model: str = "text-embedding-3-large"
    llm_model: str = "gpt-4o"
    rerank_model: str = "cross-encoder/ms-marco-MiniLM-L-2-v2"

    # Retrieval
    initial_top_k: int = 20
    rerank_top_n: int = 5
    temperature: float = 0.0

    # Monitoring
    log_queries: bool = True
    track_metrics: bool = True


class QueryMetrics(BaseModel):
    """Query execution metrics."""
    query_id: str
    question: str
    latency_ms: float
    retrieval_count: int
    timestamp: datetime


class ProductionRAGPipeline:
    """Production-ready RAG pipeline."""

    def __init__(self, config: ProductionConfig):
        self.config = config
        self.metrics: List[QueryMetrics] = []

        # Initialize Qdrant
        self.qdrant_client = QdrantClient(
            host=config.qdrant_url,
            port=config.qdrant_port,
        )

        # Configure models
        Settings.embed_model = OpenAIEmbedding(model=config.embedding_model)
        Settings.llm = OpenAI(model=config.llm_model, temperature=config.temperature)

        # Reranker
        self.reranker = SentenceTransformerRerank(
            model=config.rerank_model,
            top_n=config.rerank_top_n,
        )

        # Load or create index
        self._init_index()

    def _init_index(self):
        """Initialize vector index."""
        try:
            vector_store = QdrantVectorStore(
                client=self.qdrant_client,
                collection_name=self.config.collection_name,
            )
            self.index = VectorStoreIndex.from_vector_store(vector_store)
            logger.info(f"Loaded index: {self.config.collection_name}")
        except Exception as e:
            logger.warning(f"Could not load index: {e}")
            self.index = None

    def query(
        self,
        question: str,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Query with full production features.

        Args:
            question: User question
            filters: Metadata filters

        Returns:
            Dict with answer, sources, and metrics
        """
        if not self.index:
            raise ValueError("Index not initialized")

        query_id = str(uuid.uuid4())[:8]
        start_time = time.time()

        if self.config.log_queries:
            logger.info(f"[{query_id}] Query: {question[:100]}...")

        # Build query engine
        query_engine = self.index.as_query_engine(
            similarity_top_k=self.config.initial_top_k,
            node_postprocessors=[self.reranker],
            vector_store_kwargs={"filter": filters} if filters else {},
        )

        # Execute query
        response = query_engine.query(question)

        latency_ms = (time.time() - start_time) * 1000

        # Track metrics
        if self.config.track_metrics:
            metrics = QueryMetrics(
                query_id=query_id,
                question=question,
                latency_ms=latency_ms,
                retrieval_count=len(response.source_nodes),
                timestamp=datetime.now(),
            )
            self.metrics.append(metrics)

        if self.config.log_queries:
            logger.info(f"[{query_id}] Completed in {latency_ms:.0f}ms")

        return {
            "query_id": query_id,
            "answer": response.response,
            "sources": [
                {
                    "file": node.metadata.get("file_name", "unknown"),
                    "score": round(node.score, 4),
                    "text_preview": node.text[:200] + "...",
                }
                for node in response.source_nodes
            ],
            "latency_ms": latency_ms,
        }

    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get aggregated metrics."""
        if not self.metrics:
            return {"total_queries": 0}

        latencies = [m.latency_ms for m in self.metrics]
        return {
            "total_queries": len(self.metrics),
            "avg_latency_ms": sum(latencies) / len(latencies),
            "p95_latency_ms": sorted(latencies)[int(len(latencies) * 0.95)],
            "avg_retrieval_count": sum(m.retrieval_count for m in self.metrics) / len(self.metrics),
        }
```

### Hybrid Search Pipeline

```python
"""
Template: Hybrid Search Pipeline
Use for: Technical documentation, mixed keyword/semantic queries
"""
from dataclasses import dataclass
from typing import List, Optional

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.core.retrievers import QueryFusionRetriever


@dataclass
class HybridConfig:
    """Hybrid search configuration."""
    data_dir: str
    chunk_size: int = 512
    chunk_overlap: int = 100
    bm25_weight: float = 0.4
    vector_weight: float = 0.6
    initial_top_k: int = 20
    final_top_k: int = 5


class HybridSearchPipeline:
    """Hybrid BM25 + Vector search pipeline."""

    def __init__(self, config: HybridConfig):
        self.config = config
        self.nodes = None
        self.retriever = None

    def build_index(self) -> int:
        """Build hybrid index."""
        # Load documents
        documents = SimpleDirectoryReader(
            input_dir=self.config.data_dir,
            recursive=True,
        ).load_data()

        # Parse
        parser = SentenceSplitter(
            chunk_size=self.config.chunk_size,
            chunk_overlap=self.config.chunk_overlap,
        )
        self.nodes = parser.get_nodes_from_documents(documents)

        # Vector index
        vector_index = VectorStoreIndex(self.nodes)
        vector_retriever = vector_index.as_retriever(
            similarity_top_k=self.config.initial_top_k
        )

        # BM25 retriever
        bm25_retriever = BM25Retriever.from_defaults(
            nodes=self.nodes,
            similarity_top_k=self.config.initial_top_k,
        )

        # Fusion retriever
        self.retriever = QueryFusionRetriever(
            retrievers=[bm25_retriever, vector_retriever],
            retriever_weights=[self.config.bm25_weight, self.config.vector_weight],
            mode="reciprocal_rerank",
            similarity_top_k=self.config.final_top_k,
        )

        return len(self.nodes)

    def retrieve(self, query: str) -> List[dict]:
        """Retrieve relevant chunks."""
        if not self.retriever:
            raise ValueError("Index not built")

        results = self.retriever.retrieve(query)

        return [
            {
                "text": node.text,
                "score": node.score,
                "metadata": node.metadata,
            }
            for node in results
        ]
```

---

## Configuration Templates

### Environment Configuration

```python
"""
config.py - Environment-based configuration
"""
from pydantic_settings import BaseSettings
from typing import Optional


class RAGSettings(BaseSettings):
    """RAG configuration from environment variables."""

    # API Keys
    openai_api_key: str
    cohere_api_key: Optional[str] = None

    # Vector Database
    qdrant_url: str = "localhost"
    qdrant_port: int = 6333
    qdrant_api_key: Optional[str] = None

    # Redis Cache
    redis_url: Optional[str] = None
    cache_ttl: int = 3600

    # Models
    embedding_model: str = "text-embedding-3-large"
    llm_model: str = "gpt-4o"
    rerank_model: str = "cross-encoder/ms-marco-MiniLM-L-2-v2"

    # Chunking
    chunk_size: int = 1024
    chunk_overlap: int = 200

    # Retrieval
    top_k: int = 10
    rerank_top_n: int = 5
    similarity_threshold: float = 0.5

    # Performance
    batch_size: int = 100
    max_concurrent_requests: int = 10

    class Config:
        env_file = ".env"
        env_prefix = "RAG_"


# Usage: settings = RAGSettings()
```

### YAML Configuration

```yaml
# rag_config.yaml
# RAG Pipeline Configuration

# Document Processing
ingestion:
  source_dir: "./data"
  supported_extensions:
    - .pdf
    - .md
    - .txt
    - .docx
  exclude_patterns:
    - "*.tmp"
    - "draft_*"

chunking:
  strategy: "recursive"  # fixed, recursive, semantic
  chunk_size: 1024
  chunk_overlap: 200
  separators:
    - "\n\n"
    - "\n"
    - ". "
    - " "

# Vector Store
vector_store:
  provider: "qdrant"  # qdrant, pinecone, chroma, pgvector
  collection_name: "knowledge_base"
  distance_metric: "cosine"

  # Qdrant-specific
  qdrant:
    url: "${QDRANT_URL:-localhost}"
    port: 6333
    prefer_grpc: true

  # Pinecone-specific
  pinecone:
    environment: "us-west1-gcp"
    index_name: "my-index"

# Models
models:
  embedding:
    provider: "openai"
    model: "text-embedding-3-large"
    dimensions: 3072

  llm:
    provider: "openai"
    model: "gpt-4o"
    temperature: 0.0
    max_tokens: 4096

  reranker:
    enabled: true
    model: "cross-encoder/ms-marco-MiniLM-L-2-v2"
    top_n: 5

# Retrieval
retrieval:
  strategy: "hybrid"  # vector, bm25, hybrid
  top_k: 20
  rerank_top_n: 5

  hybrid:
    bm25_weight: 0.4
    vector_weight: 0.6
    fusion_method: "reciprocal_rerank"

  filters:
    enable_metadata_filtering: true
    enable_date_filtering: true

# Caching
cache:
  enabled: true
  provider: "redis"
  ttl_seconds: 3600
  redis_url: "${REDIS_URL:-redis://localhost:6379}"

# Monitoring
monitoring:
  log_queries: true
  track_latency: true
  track_token_usage: true
  export_metrics: true
  prometheus_port: 9090

# Rate Limiting
rate_limiting:
  enabled: true
  requests_per_minute: 60
  tokens_per_minute: 100000
```

### Configuration Loader

```python
"""
config_loader.py - Load and validate configuration
"""
import yaml
import os
from pathlib import Path
from typing import Any, Dict


def load_config(config_path: str = "rag_config.yaml") -> Dict[str, Any]:
    """
    Load configuration with environment variable substitution.
    """
    with open(config_path, 'r') as f:
        config_str = f.read()

    # Substitute environment variables
    for key, value in os.environ.items():
        config_str = config_str.replace(f"${{{key}}}", value)

    # Handle defaults: ${VAR:-default}
    import re
    pattern = r'\$\{(\w+):-([^}]*)\}'
    def replace_with_default(match):
        var_name = match.group(1)
        default = match.group(2)
        return os.environ.get(var_name, default)

    config_str = re.sub(pattern, replace_with_default, config_str)

    return yaml.safe_load(config_str)


# Usage
config = load_config("rag_config.yaml")
print(f"Chunk size: {config['chunking']['chunk_size']}")
```

---

## Prompt Templates

### Basic QA Prompt

```python
"""
Basic question-answering prompt template.
"""
BASIC_QA_PROMPT = """You are a helpful assistant. Answer the question based on the provided context.

Context:
{context}

Question: {question}

Instructions:
- Answer based only on the context provided
- If the context doesn't contain the answer, say "I don't have enough information to answer this question"
- Be concise but complete

Answer:"""
```

### Citation Prompt

```python
"""
Prompt with source citations.
"""
CITATION_PROMPT = """You are a knowledgeable assistant. Answer questions using ONLY the provided context.
Always cite your sources.

Context:
{context}

Question: {question}

Instructions:
1. Answer the question based solely on the context above
2. Cite sources using [Source: filename] format after each claim
3. If multiple sources support a claim, cite all of them
4. If the context doesn't contain the answer, say "The provided documents don't contain this information"
5. Do not make up or infer information not explicitly stated in the context

Answer with citations:"""
```

### Multi-Hop Reasoning Prompt

```python
"""
Prompt for complex questions requiring reasoning across multiple documents.
"""
MULTI_HOP_PROMPT = """You are an expert analyst. Answer complex questions by reasoning across multiple documents.

Context Documents:
{context}

Question: {question}

Instructions:
1. First, identify which documents contain relevant information
2. Extract key facts from each relevant document
3. Reason across the facts to form a complete answer
4. Show your reasoning step by step
5. Cite sources for each fact: [Source: filename]
6. If documents contain conflicting information, note the discrepancy

Analysis and Answer:"""
```

### Conversational RAG Prompt

```python
"""
Prompt for conversational/chat RAG with history.
"""
CONVERSATIONAL_PROMPT = """You are a helpful assistant having a conversation with a user.
Use the retrieved context to answer questions while maintaining conversation flow.

Previous Conversation:
{chat_history}

Retrieved Context:
{context}

Current Question: {question}

Instructions:
1. Consider the conversation history for context
2. Answer based on the retrieved documents
3. Maintain a natural conversational tone
4. Reference previous discussion points when relevant
5. Cite sources when making factual claims
6. Ask clarifying questions if the query is ambiguous

Response:"""
```

### Summarization Prompt

```python
"""
Prompt for summarizing retrieved documents.
"""
SUMMARIZATION_PROMPT = """You are an expert summarizer. Create a comprehensive summary of the retrieved documents.

Documents:
{context}

Topic/Focus: {question}

Instructions:
1. Identify the main themes across all documents
2. Extract key points and insights
3. Organize the summary logically
4. Highlight any conflicting information
5. Note gaps or areas needing more information
6. Keep the summary focused on the specified topic

Summary:"""
```

### Structured Output Prompt

```python
"""
Prompt for generating structured JSON output.
"""
STRUCTURED_OUTPUT_PROMPT = """You are an information extraction system. Extract structured information from the context.

Context:
{context}

Query: {question}

Output the answer as valid JSON with the following structure:
{{
    "answer": "Direct answer to the question",
    "confidence": "high/medium/low",
    "sources": ["list of source filenames"],
    "key_facts": ["list of supporting facts"],
    "related_topics": ["list of related topics mentioned"]
}}

If information is not available, use null for that field.

JSON Output:"""
```

### LlamaIndex PromptTemplate Usage

```python
"""
Using prompts with LlamaIndex.
"""
from llama_index.core import PromptTemplate

# Define prompt
qa_template = PromptTemplate(
    """You are a helpful assistant. Answer using only the provided context.
Always cite sources using [Source: filename] format.

Context:
{context_str}

Question: {query_str}

Answer with citations:"""
)

# Use in query engine
query_engine = index.as_query_engine(
    text_qa_template=qa_template,
    similarity_top_k=5,
)

response = query_engine.query("What is the main topic?")
```

### LangChain Prompt Usage

```python
"""
Using prompts with LangChain.
"""
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage

# Simple template
simple_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""Answer based on this context:

Context: {context}

Question: {question}

Answer:"""
)

# Chat template
chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="""You are a helpful assistant with access to a knowledge base.
Answer questions based only on the provided context.
Always cite sources using [Source: filename] format."""),
    HumanMessage(content="""Context:
{context}

Question: {question}"""),
])

# Use in chain
from langchain.chains import RetrievalQA

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    chain_type_kwargs={"prompt": simple_prompt}
)
```

---

## Evaluation Templates

### RAGAS Evaluation Setup

```python
"""
Template for RAG evaluation using RAGAS.
Requirements: pip install ragas datasets
"""
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)
from datasets import Dataset


def create_evaluation_dataset(
    questions: list[str],
    ground_truths: list[str],
    rag_pipeline,
) -> Dataset:
    """
    Create evaluation dataset from RAG pipeline.
    """
    answers = []
    contexts = []

    for question in questions:
        result = rag_pipeline.query(question)
        answers.append(result["answer"])
        contexts.append([src["text"] for src in result["sources"]])

    return Dataset.from_dict({
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths,
    })


def evaluate_rag(dataset: Dataset) -> dict:
    """
    Run RAGAS evaluation.
    """
    result = evaluate(
        dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall,
        ],
    )

    return {
        "faithfulness": result["faithfulness"],
        "answer_relevancy": result["answer_relevancy"],
        "context_precision": result["context_precision"],
        "context_recall": result["context_recall"],
    }


# Usage
if __name__ == "__main__":
    # Sample evaluation data
    questions = [
        "What is machine learning?",
        "How does RAG work?",
        "What are embeddings?",
    ]
    ground_truths = [
        "Machine learning is a subset of AI that enables systems to learn from data.",
        "RAG retrieves relevant documents and uses them to augment LLM responses.",
        "Embeddings are vector representations of text that capture semantic meaning.",
    ]

    # Create dataset
    dataset = create_evaluation_dataset(questions, ground_truths, rag_pipeline)

    # Evaluate
    scores = evaluate_rag(dataset)
    print("Evaluation Results:")
    for metric, score in scores.items():
        print(f"  {metric}: {score:.3f}")
```

### LlamaIndex Evaluation

```python
"""
Template for LlamaIndex built-in evaluation.
"""
from llama_index.core.evaluation import (
    FaithfulnessEvaluator,
    RelevancyEvaluator,
    CorrectnessEvaluator,
)
from llama_index.llms.openai import OpenAI


def evaluate_response(
    query: str,
    response,
    reference: str = None,
    llm = None,
):
    """
    Evaluate a RAG response using LlamaIndex evaluators.
    """
    llm = llm or OpenAI(model="gpt-4o", temperature=0)

    results = {}

    # Faithfulness: Is the response grounded in context?
    faithfulness_eval = FaithfulnessEvaluator(llm=llm)
    faith_result = faithfulness_eval.evaluate_response(
        query=query,
        response=response,
    )
    results["faithfulness"] = {
        "score": faith_result.score,
        "passing": faith_result.passing,
        "feedback": faith_result.feedback,
    }

    # Relevancy: Is the response relevant to the query?
    relevancy_eval = RelevancyEvaluator(llm=llm)
    rel_result = relevancy_eval.evaluate_response(
        query=query,
        response=response,
    )
    results["relevancy"] = {
        "score": rel_result.score,
        "passing": rel_result.passing,
        "feedback": rel_result.feedback,
    }

    # Correctness: Is the response correct? (requires reference)
    if reference:
        correctness_eval = CorrectnessEvaluator(llm=llm)
        corr_result = correctness_eval.evaluate(
            query=query,
            response=response.response,
            reference=reference,
        )
        results["correctness"] = {
            "score": corr_result.score,
            "passing": corr_result.passing,
            "feedback": corr_result.feedback,
        }

    return results
```

---

## Docker Deployment

### Dockerfile

```dockerfile
# Dockerfile for RAG API
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose

```yaml
# docker-compose.yaml
version: '3.8'

services:
  rag-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - RAG_QDRANT_URL=qdrant
      - RAG_QDRANT_PORT=6333
      - RAG_REDIS_URL=redis://redis:6379
    depends_on:
      - qdrant
      - redis
    volumes:
      - ./data:/app/data:ro
    restart: unless-stopped

  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_data:/qdrant/storage
    environment:
      - QDRANT__SERVICE__GRPC_PORT=6334
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes
    restart: unless-stopped

volumes:
  qdrant_data:
  redis_data:
```

### requirements.txt

```text
# requirements.txt
# Core
llama-index>=0.10.0
llama-index-llms-openai>=0.1.0
llama-index-embeddings-openai>=0.1.0
llama-index-vector-stores-qdrant>=0.1.0
llama-index-retrievers-bm25>=0.1.0

# Vector stores
qdrant-client>=1.7.0

# Web framework
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
pydantic>=2.5.0
pydantic-settings>=2.1.0

# Caching
redis>=5.0.0

# Evaluation
ragas>=0.1.0

# Utilities
python-multipart>=0.0.6
python-dotenv>=1.0.0
httpx>=0.26.0
tenacity>=8.2.0
```

### Kubernetes Deployment

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rag-api
  labels:
    app: rag-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: rag-api
  template:
    metadata:
      labels:
        app: rag-api
    spec:
      containers:
      - name: rag-api
        image: your-registry/rag-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: rag-secrets
              key: openai-api-key
        - name: RAG_QDRANT_URL
          value: "qdrant-service"
        - name: RAG_REDIS_URL
          value: "redis://redis-service:6379"
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
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: rag-api-service
spec:
  selector:
    app: rag-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```
