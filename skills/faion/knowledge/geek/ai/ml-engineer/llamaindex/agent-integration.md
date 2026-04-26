# Agent Integration — LlamaIndex

## When to use
- Building RAG over private documents: PDFs, Notion, GitHub repos, SQL databases
- Application is document-centric and retrieval quality is the primary concern
- Need LlamaParse for complex document parsing (tables, figures, multi-column PDFs)
- Building multi-step data-aware agents using `AgentWorkflow` with typed events
- Enterprise search that combines vector search, keyword search, and metadata filtering
- GraphRAG use case: entity relationships matter (e.g., contract analysis, knowledge graphs)

## When NOT to use
- Pure text orchestration without a retrieval step — LangChain or direct SDK is simpler
- Complex multi-tool agent with >10 heterogeneous tools — LangGraph offers better state management
- Real-time data streams where indexing latency is unacceptable — use streaming ingestion pipelines separately
- Team is already deep in LangChain — migration cost exceeds the retrieval quality gain
- Prototyping a simple chatbot with no private data — direct LLM call is faster to build

## Where it fails / limitations
- `VectorStoreIndex.from_documents()` on large corpora is blocking and slow; use async ingestion pipelines for >10K documents
- Default chunk size (512 tokens) and top_k (2) are too conservative for most production use cases — tune aggressively
- `PropertyGraphIndex` (GraphRAG) requires an LLM call per entity extraction — 5-10x more expensive than vector index
- LlamaHub connector quality varies: some community connectors are unmaintained or break on API changes
- `AgentWorkflow` event typing is strict; mismatched event types cause silent failures — enable `verbose=True` during development
- Evaluation metrics (`Faithfulness`, `Relevancy`) require LLM calls and are expensive to run at scale
- Persisting indexes to disk requires explicit `storage_context` setup — beginners lose index state on restart

## Agentic workflow
Use LlamaIndex as the retrieval backbone within a larger agent. A subagent receives a query, calls `query_engine.aquery()` asynchronously, and returns retrieved passages with source citations. For multi-step tasks, use `AgentWorkflow` with typed `StartEvent` → `RetrieveEvent` → `SynthesizeEvent` → `StopEvent` steps. The event-driven model maps well to agent task queues: each step emits events that the next step consumes, enabling pause/resume for human-in-loop checkpoints. For complex question decomposition, `SubQuestionQueryEngine` dispatches sub-queries in parallel.

### Recommended subagents
- `faion-sdd-executor-agent` — can be instructed to use a LlamaIndex query engine as a tool for document research steps

### Prompt pattern
```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.workflow import Workflow, StartEvent, StopEvent, step
from llama_index.llms.anthropic import Anthropic
from llama_index.embeddings.openai import OpenAIEmbedding

Settings.llm = Anthropic(model="claude-sonnet-4-5")
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

class RAGWorkflow(Workflow):
    def __init__(self, index: VectorStoreIndex, **kwargs):
        super().__init__(**kwargs)
        self.query_engine = index.as_query_engine(
            similarity_top_k=5, response_mode="compact"
        )

    @step
    async def retrieve_and_answer(self, ev: StartEvent) -> StopEvent:
        response = await self.query_engine.aquery(ev.query)
        return StopEvent(result={
            "answer": str(response),
            "sources": [n.node.get_content()[:200] for n in response.source_nodes],
        })
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `llama-index` | Core framework | `pip install llama-index` / [docs](https://docs.llamaindex.ai/) |
| `llama-parse` | Advanced PDF/doc parsing (SaaS) | `pip install llama-parse` / [docs](https://docs.llamaindex.ai/en/stable/llama_cloud/llama_parse/) |
| `llama-index-workflows` | Standalone workflow engine | `pip install llama-index-workflows` |
| `llama-index-vector-stores-qdrant` | Qdrant backend | `pip install llama-index-vector-stores-qdrant` |
| `llama-index-llms-anthropic` | Claude LLM integration | `pip install llama-index-llms-anthropic` |
| LlamaCloud CLI | Managed indexing + retrieval (SaaS) | [cloud.llamaindex.ai](https://cloud.llamaindex.ai) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| LlamaCloud | SaaS | Yes | Managed indexing; LlamaParse included; production-grade pipeline |
| LlamaParse | SaaS | Yes | $3/1000 pages; best PDF table/figure extraction available |
| LlamaHub | OSS (connectors) | Yes | 1500+ data connectors; quality varies by connector |
| Qdrant | OSS + SaaS | Yes | Best self-hosted vector store for LlamaIndex production |
| Pinecone | SaaS | Yes | Managed, serverless; pair with `llama-index-vector-stores-pinecone` |
| Chroma | OSS | Yes | Local dev; simple API; not for multi-process production |

## Templates & scripts
```python
# persist_index.py — build index once, reload cheaply (≤40 lines)
import os
from llama_index.core import (
    VectorStoreIndex, SimpleDirectoryReader,
    StorageContext, load_index_from_storage, Settings
)
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

INDEX_DIR = "./storage"
Settings.llm = OpenAI(model="gpt-4o-mini", temperature=0)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
Settings.chunk_size = 512
Settings.chunk_overlap = 50

def get_or_build_index(docs_dir: str) -> VectorStoreIndex:
    if os.path.exists(INDEX_DIR):
        storage_context = StorageContext.from_defaults(persist_dir=INDEX_DIR)
        return load_index_from_storage(storage_context)
    documents = SimpleDirectoryReader(docs_dir).load_data()
    index = VectorStoreIndex.from_documents(documents, show_progress=True)
    index.storage_context.persist(persist_dir=INDEX_DIR)
    return index

index = get_or_build_index("./data")
query_engine = index.as_query_engine(similarity_top_k=5)
response = query_engine.query("What is the refund policy?")
print(response)
```

## Best practices
- Set `similarity_top_k=5` to `10` and `response_mode="refine"` for complex questions; defaults are too conservative
- Use `HierarchicalNodeParser` for long documents: embed small child nodes, retrieve parent context for synthesis
- Persist indexes with `storage_context.persist()` — in-memory indexes are lost on process restart
- Async all the way: use `aquery()`, `aretrieve()` for all production code; sync calls block event loops
- Add metadata at ingestion: `Document(text=..., metadata={"source": "contracts/2025/..."})` enables metadata filtering
- For hybrid search, use Qdrant or Weaviate with `QdrantVectorStore(enable_hybrid=True)` — BM25 + vector in one call
- Track token usage with `TokenCountingHandler` callback; set cost alerts before deploying expensive PropertyGraphIndex
- Use `SubQuestionQueryEngine` for multi-part user questions; it decomposes and parallelizes sub-queries

## AI-agent gotchas
- `AgentWorkflow` event types must match exactly between steps — a typo in the event class name causes a silent no-op
- `from_documents()` calls LLM for metadata extraction by default in some configurations — disable with `metadata_extractor=None` if unexpected API costs appear
- LlamaParse rate limits at ~200 pages/minute on free tier; implement retry with exponential backoff for bulk ingestion
- Default embedding model is `text-davinci-003` in old configs — always set `Settings.embed_model` explicitly
- Index persistence format changes between LlamaIndex minor versions; re-index if you upgrade across major versions
- `SimpleDirectoryReader` follows symlinks by default — can ingest unintended files; set `recursive=False` or use explicit file list
- `SubQuestionQueryEngine` runs sub-queries sequentially by default; pass `use_async=True` to parallelize

## References
- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- [LlamaIndex GitHub](https://github.com/run-llama/llama_index)
- [LlamaHub Connectors](https://llamahub.ai/)
- [LlamaParse](https://docs.llamaindex.ai/en/stable/llama_cloud/llama_parse/)
- [AgentWorkflow Blog Post](https://www.llamaindex.ai/blog/introducing-agentworkflow-a-powerful-system-for-building-ai-agent-systems)
- [Building Performant RAG](https://developers.llamaindex.ai/python/framework/optimizing/production_rag/)
- [Property Graph Index Guide](https://docs.llamaindex.ai/en/stable/module_guides/indexing/lpg_index_guide/)
