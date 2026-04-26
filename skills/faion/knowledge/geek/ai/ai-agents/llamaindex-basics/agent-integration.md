# Agent Integration — LlamaIndex Basics

## When to use
- Building a RAG pipeline over a static or semi-static document corpus (PDFs, Markdown, DOCX)
- Implementing document Q&A where retrieval quality matters more than workflow complexity
- Prototype needs to be operational in <50 lines — LlamaIndex defaults cover most tuning later
- The corpus is already on disk or accessible via URL; no real-time streaming ingestion needed
- You need node-level metadata (titles, keywords, summaries) auto-extracted before indexing

## When NOT to use
- Complex multi-step workflows with branching logic — use LangGraph instead
- You need agent-driven tool use as the primary concern — LlamaIndex agents exist but LangGraph is more expressive
- Real-time streaming ingestion (Kafka, CDC) — LlamaIndex ingestion pipeline is batch-oriented
- The task is pure LLM generation with no retrieval — plain Anthropic SDK is lighter
- Team already standardized on LangChain; mixing both frameworks adds maintenance overhead

## Where it fails / limitations
- SemanticSplitterNodeParser requires an embedding call per sentence boundary — expensive on large corpora
- VectorStoreIndex held in memory is not persistent across restarts without explicit `storage_context.persist()`
- `SimpleDirectoryReader` has no incremental sync; re-ingesting modified files duplicates nodes without dedup logic
- LlamaHub reader quality varies; community readers may lag behind upstream API changes
- Default `gpt-4o` / `text-embedding-3-small` hardcodes OpenAI — must override `Settings.llm` and `Settings.embed_model` explicitly to use Claude or other providers
- Chunk overlap set too high relative to chunk size causes near-duplicate nodes that inflate index size and retrieval noise

## Agentic workflow
An agent receives a task requiring document lookup, invokes LlamaIndex to build or load an index, then queries the index and returns structured results. The agent owns orchestration (retry, fallback, output validation); LlamaIndex owns retrieval. For pipeline tasks a subagent can own the full ingestion step — load → parse → index → persist — and return a storage path the query subagent then loads. This separation keeps each agent's responsibility narrow and testable.

### Recommended subagents
- `faion-rag-agent` — builds and queries LlamaIndex pipelines; handles ingestion and response synthesis
- General research subagent — accepts a query string, loads a pre-built persistent index, returns top-k nodes + synthesized answer

### Prompt pattern
```
You are a document retrieval agent. Given the storage path "{index_path}", load the existing
VectorStoreIndex and answer: "{query}". Return JSON: {"answer": str, "sources": [{"text": str, "score": float}]}.
```

```
Ingest all files in directory "{input_dir}" using SentenceSplitter(chunk_size=512, chunk_overlap=100),
embed with text-embedding-3-small, persist to "{output_dir}". Report node count and any parse errors.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `llama-index` | Core framework | `pip install llama-index` / https://docs.llamaindex.ai |
| `llama-index-cli` | CLI for ingestion / query debug | bundled with `llama-index` |
| `llamactl` | LlamaCloud index management | `pip install llama-cloud` / https://cloud.llamaindex.ai |
| `llama-hub` | Browse 1500+ connectors | https://llamahub.ai |
| `llama-parse` | Cloud PDF/DOCX parser | `pip install llama-parse` / https://llamaparse.ai |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| LlamaCloud | SaaS | Yes | Managed indexing + LlamaParse; REST API |
| Qdrant | OSS | Yes | Native LlamaIndex vector store integration |
| Pinecone | SaaS | Yes | `llama-index-vector-stores-pinecone` |
| Chroma | OSS | Yes | Good for local dev; `chromadb` |
| Weaviate | OSS/SaaS | Yes | `llama-index-vector-stores-weaviate` |
| pgvector | OSS | Yes | `llama-index-vector-stores-postgres` |
| Langfuse | OSS/SaaS | Yes | Observability via `llama-index-instrumentation-langfuse` |
| Arize Phoenix | OSS | Yes | LLM tracing with LlamaIndex callbacks |

## Templates & scripts
See `templates.md` for ingestion pipeline templates. Inline minimal persistent-index script:

```python
import os, sys
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext, load_index_from_storage
from llama_index.llms.anthropic import Anthropic
from llama_index.embeddings.openai import OpenAIEmbedding

Settings.llm = Anthropic(model="claude-opus-4-5")
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

PERSIST_DIR = "./index_storage"
INPUT_DIR = sys.argv[1] if len(sys.argv) > 1 else "./data"

if os.path.exists(PERSIST_DIR):
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)
else:
    docs = SimpleDirectoryReader(INPUT_DIR, recursive=True).load_data()
    index = VectorStoreIndex.from_documents(docs)
    index.storage_context.persist(PERSIST_DIR)

qe = index.as_query_engine(similarity_top_k=5, response_mode="compact")
print(qe.query(sys.argv[2] if len(sys.argv) > 2 else "Summarize the content."))
```

## Best practices
- Always persist the index to disk after first build — re-embedding on every run costs tokens and time
- Set `Settings.llm` and `Settings.embed_model` globally at startup, not per-index, to avoid accidental model mixing
- Use `IngestionPipeline` with `TitleExtractor` + `KeywordExtractor` for any corpus used in production retrieval; metadata improves filter-based retrieval precision significantly
- For large corpora (>10k docs), point the vector store at Qdrant or Pinecone — in-memory index will OOM
- Tune `chunk_size` per content type: 256-512 for factual Q&A, 1024-2048 for summarization tasks
- Add a `SimilarityPostprocessor(similarity_cutoff=0.7)` to drop low-confidence nodes before synthesis — prevents hallucination from weak context
- Use `query_engine.aquery()` (async) when serving multiple users; sync queries block the event loop
- Never trust node scores alone — always inspect `response.source_nodes` in evaluation to verify retrieval quality

## AI-agent gotchas
- LLM-as-extractor in `QuestionsAnsweredExtractor` and `SummaryExtractor` adds latency proportional to node count — run extraction as a one-time offline batch, not inline during agent queries
- `ReActAgent` in LlamaIndex uses a fixed loop; set `max_iterations` explicitly or the agent can spin on ambiguous tool descriptions
- `SimpleDirectoryReader` silently skips unsupported file types — log `len(documents)` after load and fail-fast if count is zero
- Embedding model rate limits hit fast during bulk ingestion — add a `RateLimiter` or batch with `asyncio.gather` + semaphore
- LlamaIndex's default `response_mode="compact"` truncates context to fit the model's context window without warning; switch to `"tree_summarize"` for long documents where truncation risks dropping critical content
- Persistent index loaded from disk will not reflect document updates — implement a version hash or mtime check to trigger re-indexing

## References
- https://docs.llamaindex.ai/en/stable/
- https://llamahub.ai/
- https://github.com/run-llama/llama_index
- https://cloud.llamaindex.ai/
- "Building LLM Apps with LlamaIndex" — LlamaIndex official blog series
