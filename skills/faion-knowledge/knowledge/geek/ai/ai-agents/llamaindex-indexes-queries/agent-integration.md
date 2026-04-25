# Agent Integration — LlamaIndex Indexes & Query Engines

## When to use
- Building a RAG pipeline that requires multiple index types over the same corpus (vector + keyword + graph)
- Queries span heterogeneous data sources: SQL tables + unstructured documents + knowledge graphs
- Need hierarchical summarization (TreeIndex, SummaryIndex) over large document sets
- Building an agent with knowledge retrieval tools backed by LlamaIndex query engines
- Complex multi-hop questions that benefit from SubQuestionQueryEngine decomposition
- When you need structured output (Pydantic) from document queries with schema enforcement

## When NOT to use
- Simple single-document Q&A — direct prompt + context is faster and cheaper
- High-throughput production APIs where LlamaIndex's Python overhead matters — use a dedicated vector DB SDK directly
- When you only need BM25 keyword search — Elasticsearch or Typesense is lighter
- If the codebase already uses LangChain RAG heavily — mixing both frameworks adds cognitive overhead without clear gain
- Real-time streaming over very large retrievals — latency compounds with each response synthesis pass

## Where it fails / limitations
- RouterQueryEngine LLM routing occasionally selects the wrong index when tool descriptions are similar — requires careful metadata naming
- SubQuestionQueryEngine over-decomposes simple questions, doubling token cost for no quality gain
- KnowledgeGraphIndex extraction quality is fully dependent on the LLM prompt — relationship hallucination is common without schema constraints
- Auto-merging retriever requires strict HierarchicalNodeParser setup; mismatched chunk sizes silently produce no merges
- Persistent index reloading (from_vector_store) can fail silently if the collection schema changed between index creation and load
- SummaryIndex passes all nodes to the LLM, making it unusable beyond ~100 small documents before context overflow

## Agentic workflow
Use LlamaIndex query engines as tools inside a Claude or LangGraph agent: wrap each query engine in a `QueryEngineTool` with a precise natural-language description, then register the tools with the agent. The agent routes to the right index based on query type (structured data → SQL engine, unstructured → vector engine, multi-source → SubQuestion engine). For research agents, use `SubQuestionQueryEngine` to decompose the task and retrieve from specialized indexes in parallel (`use_async=True`), then synthesize results with `tree_summarize` mode.

### Recommended subagents
- `index-builder` — ingests documents, selects index type, persists to storage (run once per corpus)
- `query-router` — wraps multiple QueryEngineTools, routes user questions to the right index
- `synthesizer` — takes retrieved nodes, applies structured output (Pydantic) or custom prompts to produce final answer
- `reranker` — post-processes retrieved nodes with cross-encoder or Cohere reranker before synthesis

### Prompt pattern
```
You are a knowledge retrieval agent. You have these tools:
- tech_docs: Search technical documentation for implementation details
- financial_data: Query financial tables for numeric metrics
- knowledge_graph: Traverse entity relationships in the knowledge base

Answer the user's question by selecting the right tool(s).
Question: {question}
```

```python
# Minimal QueryEngineTool registration
from llama_index.core.tools import QueryEngineTool, ToolMetadata

tools = [
    QueryEngineTool(
        query_engine=vector_index.as_query_engine(similarity_top_k=5),
        metadata=ToolMetadata(
            name="product_docs",
            description="Product documentation: features, API reference, troubleshooting",
        ),
    ),
]
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `llama-index-core` | Core framework | `pip install llama-index-core` / https://docs.llamaindex.ai/ |
| `llama-index-vector-stores-qdrant` | Qdrant persistent storage | `pip install llama-index-vector-stores-qdrant` |
| `llama-index-postprocessor-cohere-rerank` | Cohere reranking | `pip install llama-index-postprocessor-cohere-rerank` |
| `llama-index-retrievers-bm25` | BM25 hybrid retrieval | `pip install llama-index-retrievers-bm25` |
| `qdrant-client` | Qdrant vector DB client | `pip install qdrant-client` / https://qdrant.tech/docs/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Qdrant | SaaS/OSS | Yes | Best production vector store for LlamaIndex; supports filtering + HNSW |
| Pinecone | SaaS | Yes | Managed serverless; good for variable-load agents |
| Weaviate | SaaS/OSS | Yes | Hybrid vector + keyword built-in; use for teams needing schema enforcement |
| Cohere | SaaS | Yes | Reranker API; drop-in quality boost, ~$0.001/query |
| Neo4j | SaaS/OSS | Yes | Production graph store for KnowledgeGraphIndex |
| Arize Phoenix | OSS | Yes | LlamaIndex-native tracing and evaluation; no API key needed |

## Templates & scripts
See `templates.md` for full hybrid retriever and production pipeline templates.

Minimal hybrid retrieval setup:
```python
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.retrievers import QueryFusionRetriever
from llama_index.retrievers.bm25 import BM25Retriever

# Build both retrievers from same node set
nodes = index._docstore.docs.values()
bm25 = BM25Retriever.from_defaults(nodes=list(nodes), similarity_top_k=10)
vector = index.as_retriever(similarity_top_k=10)

hybrid = QueryFusionRetriever(
    retrievers=[bm25, vector],
    retriever_weights=[0.3, 0.7],
    num_queries=1,
    mode="reciprocal_rerank",
)
```

## Best practices
- Always retrieve more nodes than you need (similarity_top_k=20), then rerank down to top 5 — retrieval recall > synthesis precision
- Use `compact` response mode for 90% of cases; switch to `refine` only when source fidelity matters (legal, medical)
- Store index metadata (creation time, source hash) alongside the vector store — detect stale indexes before agent use
- For KnowledgeGraphIndex, provide explicit relationship type schema in the extraction prompt; unconstrained extraction produces noisy graphs
- Persist BM25 retriever nodes separately from vector index — they live in memory by default and rebuild from scratch on restart
- Use `use_async=True` in SubQuestionQueryEngine — synchronous decomposition with 5+ sub-questions is a latency killer
- Tag every query with a request ID and log retrieved node IDs — essential for debugging wrong answers in production

## AI-agent gotchas
- `response.source_nodes` is empty when `no_text` response mode is used — agents relying on citations will silently produce unsourced answers
- Updating a persistent index with new documents does not remove stale nodes — agents will retrieve outdated content; implement explicit deletion or collection versioning
- LLM router in RouterQueryEngine is a full LLM call — at high QPS, routing alone becomes a bottleneck; cache routing decisions for repeated query patterns
- SubQuestionQueryEngine may run sub-questions against wrong tools if tool descriptions overlap — test routing explicitly with unit queries before production
- Human-in-the-loop checkpoint: when agents use NLSQLTableQueryEngine, always show the generated SQL to a human before executing on write-capable connections
- Reranker APIs (Cohere) are synchronous in LlamaIndex's default integration — use async wrappers in high-concurrency agent loops

## References
- LlamaIndex docs: https://docs.llamaindex.ai/
- LlamaIndex query engines: https://docs.llamaindex.ai/en/stable/module_guides/querying/
- Hybrid retrieval guide: https://docs.llamaindex.ai/en/stable/examples/retrievers/bm25_retriever/
- Auto-merging retriever: https://docs.llamaindex.ai/en/stable/examples/retrievers/auto_merging_retriever/
- Arize Phoenix tracing: https://docs.arize.com/phoenix/integrations/llamaindex
