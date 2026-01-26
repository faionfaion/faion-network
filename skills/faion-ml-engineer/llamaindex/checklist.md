# LlamaIndex Checklists

Production-ready checklists for LlamaIndex projects.

---

## Project Setup Checklist

### Environment Configuration

- [ ] Python 3.10+ installed
- [ ] Virtual environment created (`uv venv` or `python -m venv`)
- [ ] Core package installed: `pip install llama-index`
- [ ] Environment variables configured:
  - [ ] `OPENAI_API_KEY` (if using OpenAI)
  - [ ] `ANTHROPIC_API_KEY` (if using Claude)
  - [ ] `GOOGLE_API_KEY` (if using Gemini)

### Dependencies Selection

- [ ] LLM provider package installed:
  - [ ] `llama-index-llms-openai` (recommended)
  - [ ] `llama-index-llms-anthropic`
  - [ ] `llama-index-llms-ollama`
- [ ] Embedding provider installed:
  - [ ] `llama-index-embeddings-openai` (recommended)
  - [ ] `llama-index-embeddings-huggingface`
- [ ] Vector store package installed:
  - [ ] `llama-index-vector-stores-qdrant` (production)
  - [ ] `llama-index-vector-stores-chroma` (development)
  - [ ] `llama-index-vector-stores-pinecone` (serverless)
- [ ] Additional readers installed (as needed):
  - [ ] `llama-index-readers-file`
  - [ ] `llama-index-readers-web`

### Global Settings

```python
from llama_index.core import Settings

# Verify these are set
Settings.llm = ...           # LLM instance
Settings.embed_model = ...   # Embedding model
Settings.chunk_size = 512    # Chunk size in tokens
Settings.chunk_overlap = 50  # Overlap between chunks
```

### Project Structure

```
project/
├── src/
│   ├── __init__.py
│   ├── config.py          # Settings, API keys
│   ├── data_loader.py     # Document loading
│   ├── index_builder.py   # Index creation
│   ├── query_engine.py    # Query logic
│   └── workflow.py        # Workflow definitions
├── data/
│   └── documents/         # Source documents
├── storage/
│   └── index/            # Persisted index
├── tests/
│   ├── test_retrieval.py
│   └── test_responses.py
├── .env                   # Environment variables
├── requirements.txt
└── README.md
```

---

## Index Design Checklist

### Data Assessment

- [ ] Document types identified (PDF, DOCX, MD, etc.)
- [ ] Total document count estimated
- [ ] Average document size measured
- [ ] Update frequency determined (static vs dynamic)
- [ ] Access patterns analyzed (search types)

### Index Type Selection

| Use Case | Index Type | When to Use |
|----------|------------|-------------|
| General Q&A | VectorStoreIndex | Default choice |
| Entity relationships | PropertyGraphIndex | Legal, medical, research |
| Keyword search | KeywordTableIndex | Exact term matching |
| Summarization | SummaryIndex | Small document sets |
| Mixed content | ComposableGraph | Multiple document types |

- [ ] Primary index type selected
- [ ] Secondary index considered (if hybrid needed)
- [ ] Graph index evaluated (if entity extraction needed)

### Chunking Strategy

- [ ] Chunk size determined:
  - [ ] 256-512 tokens: Precise retrieval, Q&A
  - [ ] 512-1024 tokens: General purpose (default)
  - [ ] 1024-2048 tokens: Summarization, broad context
- [ ] Overlap percentage set (10-20% of chunk size)
- [ ] Splitter type selected:
  - [ ] `SentenceSplitter`: General text
  - [ ] `SemanticSplitter`: Topic boundaries
  - [ ] `MarkdownNodeParser`: Structured docs
  - [ ] `CodeSplitter`: Source code
- [ ] Metadata extraction configured:
  - [ ] Title extraction
  - [ ] Keyword extraction
  - [ ] Summary extraction (if needed)

### Embedding Selection

| Model | Dimensions | Quality | Speed | Cost |
|-------|------------|---------|-------|------|
| text-embedding-3-small | 1536 | Good | Fast | Low |
| text-embedding-3-large | 3072 | Excellent | Medium | Medium |
| HuggingFace (local) | Varies | Good | Varies | Free |
| Cohere embed-v3 | 1024 | Excellent | Fast | Medium |

- [ ] Embedding model selected based on:
  - [ ] Quality requirements
  - [ ] Latency requirements
  - [ ] Cost constraints
  - [ ] Privacy requirements (local vs API)
- [ ] Embedding dimensions match vector store config
- [ ] Batch processing configured for large datasets

### Vector Store Selection

| Store | Best For | Managed | Hybrid Search |
|-------|----------|---------|---------------|
| Qdrant | Production self-hosted | Optional | Yes |
| Pinecone | Serverless, scale | Yes | Yes |
| Weaviate | Knowledge graphs | Optional | Yes |
| Chroma | Development | No | Limited |
| pgvector | PostgreSQL existing | No | No |

- [ ] Vector store selected
- [ ] Collection/index created
- [ ] Connection credentials secured
- [ ] Backup strategy defined

---

## Query Engine Configuration Checklist

### Basic Configuration

```python
query_engine = index.as_query_engine(
    similarity_top_k=5,        # Number of chunks
    response_mode="compact",   # Synthesis mode
    streaming=False,           # Enable streaming
)
```

- [ ] `similarity_top_k` tuned (start with 5, adjust based on eval)
- [ ] Response mode selected:
  - [ ] `compact`: Fast, good default
  - [ ] `refine`: Higher accuracy, more tokens
  - [ ] `tree_summarize`: Large retrievals
- [ ] Streaming enabled if needed for UX

### Retrieval Enhancement

- [ ] Hybrid retrieval evaluated:
  - [ ] BM25 + Vector fusion
  - [ ] Weight tuning (e.g., 0.4 BM25, 0.6 vector)
- [ ] Reranking configured:
  - [ ] Cross-encoder model selected
  - [ ] Rerank top_n configured
- [ ] Auto-merging evaluated (for hierarchical chunks)

### Query Routing (Multi-Index)

- [ ] Router type selected:
  - [ ] `LLMSingleSelector`: LLM picks one index
  - [ ] `LLMMultiSelector`: LLM picks multiple
  - [ ] `PydanticSelector`: Structured selection
- [ ] Query engine tools defined with clear descriptions
- [ ] Fallback behavior configured

### Response Quality

- [ ] Custom prompts created (if needed):
  - [ ] QA prompt template
  - [ ] Refine prompt template
- [ ] Structured output configured (if needed)
- [ ] Citation/source tracking enabled
- [ ] Confidence scoring considered

---

## Workflow Design Checklist

### Workflow Architecture

- [ ] Steps identified and documented
- [ ] Events defined (inputs/outputs per step)
- [ ] State requirements analyzed
- [ ] Parallel processing opportunities identified
- [ ] Error handling planned

### Event Design

```python
from pydantic import BaseModel, Field

class QueryEvent(BaseModel):
    """User query event."""
    query: str = Field(..., description="User's question")
    context: dict = Field(default_factory=dict)
```

- [ ] Events are Pydantic models
- [ ] Clear descriptions on all fields
- [ ] Validation rules defined
- [ ] Optional vs required fields distinguished

### Step Implementation

```python
from llama_index.core.workflow import Workflow, step

class RAGWorkflow(Workflow):
    @step
    async def retrieve(self, ev: QueryEvent) -> RetrievalEvent:
        # Implementation
        pass
```

- [ ] Steps are `async` functions
- [ ] Input/output types explicit
- [ ] Error handling in each step
- [ ] Logging/observability added

### State Management

- [ ] Global context usage planned:
  - [ ] `ctx.set()` for storing values
  - [ ] `ctx.get()` for retrieving values
- [ ] Event collection configured (`ctx.collect_events()`)
- [ ] State persistence strategy (for long-running)

---

## Agent Design Checklist

### Single Agent

- [ ] Agent type selected:
  - [ ] `ReActAgent`: Reasoning + Acting
  - [ ] `OpenAIAgent`: Function calling
  - [ ] `FunctionCallingAgent`: Generic function calling
- [ ] Tools defined:
  - [ ] Query engine tools
  - [ ] Function tools
  - [ ] API tools
- [ ] System prompt crafted
- [ ] Memory configured (chat buffer, vector)

### Multi-Agent (AgentWorkflow)

- [ ] Agent roles defined
- [ ] Handoff conditions specified
- [ ] Initial agent selected
- [ ] State shared appropriately
- [ ] Orchestration pattern chosen:
  - [ ] Sequential handoff
  - [ ] Orchestrator (meta-agent)
  - [ ] Hierarchical

### Tool Design

```python
from llama_index.core.tools import FunctionTool

def search_database(query: str, limit: int = 10) -> list:
    """Search the database for relevant records.

    Args:
        query: Search query string
        limit: Maximum results to return

    Returns:
        List of matching records
    """
    pass

tool = FunctionTool.from_defaults(fn=search_database)
```

- [ ] Tool descriptions are clear and specific
- [ ] Parameters have type hints
- [ ] Docstrings explain usage
- [ ] Error handling in tool functions

---

## Production Deployment Checklist

### Performance Optimization

- [ ] Async operations used throughout
- [ ] Batch processing for bulk operations
- [ ] Connection pooling configured (database/vector store)
- [ ] Index loaded at startup (avoid cold starts)

### Caching Strategy

- [ ] Embedding cache configured:
  ```python
  Settings.embed_model.cache_folder = "./embedding_cache"
  ```
- [ ] Response cache considered (Redis, etc.)
- [ ] Index persistence configured:
  ```python
  index.storage_context.persist(persist_dir="./storage")
  ```

### Observability

- [ ] Logging configured (structured JSON)
- [ ] Tracing enabled:
  ```python
  from llama_index.core.callbacks import CallbackManager, LlamaDebugHandler
  debug_handler = LlamaDebugHandler()
  Settings.callback_manager = CallbackManager([debug_handler])
  ```
- [ ] Metrics collected:
  - [ ] Query latency
  - [ ] Token usage
  - [ ] Retrieval hit rate
  - [ ] Error rate
- [ ] External observability integration:
  - [ ] Langfuse
  - [ ] Arize Phoenix
  - [ ] LangSmith

### Error Handling

- [ ] Retry logic with exponential backoff:
  ```python
  from tenacity import retry, stop_after_attempt, wait_exponential

  @retry(stop=stop_after_attempt(3), wait=wait_exponential())
  def query_with_retry(question):
      return query_engine.query(question)
  ```
- [ ] Fallback responses configured
- [ ] Rate limiting handled
- [ ] Timeout configuration set

### Security

- [ ] API keys in environment variables (not code)
- [ ] Secrets manager integration (optional)
- [ ] Input validation on queries
- [ ] Output sanitization (PII filtering)
- [ ] Access control for multi-tenant

### Scaling

- [ ] Horizontal scaling plan (multiple instances)
- [ ] Vector store scaling (sharding, replicas)
- [ ] Load balancing configured
- [ ] Autoscaling policies defined
- [ ] Cost monitoring enabled

### Monitoring & Alerting

- [ ] Health check endpoint
- [ ] Latency thresholds defined
- [ ] Error rate alerts
- [ ] Token usage alerts (cost control)
- [ ] Index freshness monitoring

---

## Evaluation Checklist

### Retrieval Evaluation

- [ ] Test dataset created:
  ```python
  from llama_index.core.evaluation import generate_question_context_pairs
  qa_dataset = generate_question_context_pairs(nodes, num_questions_per_chunk=2)
  ```
- [ ] Metrics tracked:
  - [ ] MRR (Mean Reciprocal Rank)
  - [ ] Hit Rate
  - [ ] NDCG (if available)
- [ ] Baseline established
- [ ] Improvement targets set

### Response Evaluation

- [ ] Evaluators configured:
  - [ ] `FaithfulnessEvaluator`: Grounding
  - [ ] `RelevancyEvaluator`: Relevance
  - [ ] `CorrectnessEvaluator`: Accuracy (needs ground truth)
- [ ] Batch evaluation pipeline:
  ```python
  from llama_index.core.evaluation import BatchEvalRunner
  runner = BatchEvalRunner(evaluators={"faith": faith_eval, "rel": rel_eval})
  ```
- [ ] Regular evaluation schedule

### A/B Testing

- [ ] Variant tracking implemented
- [ ] Statistical significance thresholds defined
- [ ] Rollback procedure documented
- [ ] Winner selection criteria clear

---

## Maintenance Checklist

### Regular Tasks

- [ ] **Daily:**
  - [ ] Monitor error rates
  - [ ] Check latency metrics
- [ ] **Weekly:**
  - [ ] Review token usage/costs
  - [ ] Run evaluation suite
  - [ ] Check for library updates
- [ ] **Monthly:**
  - [ ] Full system backup
  - [ ] Performance audit
  - [ ] Security review

### Update Procedures

- [ ] Dependency update process documented
- [ ] Index rebuild procedure documented
- [ ] Rollback procedure tested
- [ ] Changelog maintained

---

*LlamaIndex Checklists v2.0 - 2026-01-25*
