# Agent Integration — LlamaIndex Patterns

## When to use
- Advanced RAG requiring hybrid retrieval (vector + keyword), reranking, or hierarchical chunking
- Multi-document analysis where an agent must compare, correlate, or synthesize across many sources
- Structured data querying — NL-to-SQL via `NLSQLTableQueryEngine` where SQL schema is known upfront
- Chat-over-documents use case where conversation history and contextual follow-up matter
- Production system that needs LlamaIndex evaluation (faithfulness, relevancy) as an automated quality gate

## When NOT to use
- Simple single-document lookup — basic `VectorStoreIndex.from_documents()` from `llamaindex-basics` suffices
- Fully dynamic data with real-time updates — LlamaIndex indexes are append-friendly but not designed for continuous stream ingestion
- The primary task is workflow orchestration, not retrieval — LangGraph is the right choice
- Cost is a hard constraint and the corpus is small — in-memory index with no metadata extraction is cheaper
- Database is large and schema is complex/dynamic — dedicated text-to-SQL services (Vanna, SQLAI) handle schema evolution better

## Where it fails / limitations
- `QueryFusionRetriever` with `num_queries=4` generates 4 LLM calls per user query — quadruples retrieval cost
- `AutoMergingRetriever` requires hierarchical node parsing at ingestion time; changing strategy post-ingestion requires full re-index
- `SubQuestionQueryEngine` decomposition quality depends heavily on the LLM; weaker models produce poorly formed sub-questions
- `NLSQLTableQueryEngine` generates SQL without validation — malformed or unsafe SQL can execute against the database
- `SentenceTransformerRerank` runs a local cross-encoder model — adds 100-500ms latency per query on CPU; requires GPU for production throughput
- Evaluation methods (`FaithfulnessEvaluator`, `RelevancyEvaluator`) use LLM calls — batch evaluation of 100 questions costs significant tokens

## Agentic workflow
An agent using LlamaIndex patterns selects the retrieval strategy based on query characteristics: simple factual → vector retrieval, multi-document comparison → SubQuestionQueryEngine, SQL data → NLSQLTableQueryEngine. A planner subagent decides the strategy; a retriever subagent executes it; a synthesis subagent formats the result. For production, wrap evaluation in a post-query hook: if faithfulness score < 0.7, the pipeline flags the response for human review before delivery.

### Recommended subagents
- `faion-rag-agent` — owns index creation, retrieval strategy selection, response synthesis, and optional evaluation pass
- General research subagent — takes query + index path, selects between VectorRetriever / QueryFusion / SubQuestion based on query complexity

### Prompt pattern
```
You are a multi-document research agent. Load indexes from paths {index_paths}.
For query "{query}":
1. If query compares multiple sources → use SubQuestionQueryEngine across all indexes
2. If query is factual about one source → use VectorRetriever on the relevant index
3. Always rerank top-20 to top-5 before synthesis
Return JSON: {"answer": str, "strategy_used": str, "sources": [{"index": str, "text": str}]}
```

```
Evaluate the last query response for faithfulness and relevancy.
faithfulness_threshold: 0.75, relevancy_threshold: 0.70
If either score is below threshold, return {"pass": false, "reason": str}.
Otherwise return {"pass": true}.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `llama-index` | Core framework with all pattern primitives | `pip install llama-index` |
| `llama-index-postprocessor-flag-embedding-reranker` | Flag/FlagEmbedding reranker | `pip install llama-index-postprocessor-flag-embedding-reranker` |
| `sentence-transformers` | Local cross-encoder for SentenceTransformerRerank | `pip install sentence-transformers` |
| `llama-parse` | Cloud PDF parsing for complex documents | `pip install llama-parse` |
| `sqlalchemy` | Database connectivity for NLSQLTableQueryEngine | `pip install sqlalchemy` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| LlamaCloud | SaaS | Yes | Managed indexing with auto reranking and pipeline |
| Qdrant | OSS | Yes | Best OSS vector store for hybrid search with LlamaIndex |
| Pinecone | SaaS | Yes | Supports metadata filtering for partitioned retrieval |
| Cohere Rerank | SaaS | Yes | Drop-in reranker; `CohereRerank` postprocessor |
| Arize Phoenix | OSS | Yes | Traces each retrieval step including rerank scores |
| Langfuse | OSS/SaaS | Yes | End-to-end tracing with LlamaIndex instrumentation |
| PostgreSQL + pgvector | OSS | Yes | Unified vector + relational for NL-to-SQL + RAG |

## Templates & scripts
See `templates.md` for full retrieval pipeline templates. Inline hybrid retrieval with reranking:

```python
from llama_index.core import VectorStoreIndex, Settings
from llama_index.core.retrievers import QueryFusionRetriever
from llama_index.core.postprocessor import SentenceTransformerRerank
from llama_index.core.query_engine import RetrieverQueryEngine

reranker = SentenceTransformerRerank(
    model="cross-encoder/ms-marco-MiniLM-L-12-v2", top_n=5
)

vector_retriever = index.as_retriever(similarity_top_k=20)

fusion_retriever = QueryFusionRetriever(
    retrievers=[vector_retriever],
    similarity_top_k=20,
    num_queries=3,
    mode="reciprocal_rerank",
    use_async=True,
)

query_engine = RetrieverQueryEngine(
    retriever=fusion_retriever,
    node_postprocessors=[reranker],
)

response = query_engine.query("What are the key findings?")
for node in response.source_nodes:
    print(f"Score {node.score:.3f}: {node.text[:100]}")
```

## Best practices
- Default to `QueryFusionRetriever` with `num_queries=2` (not 4) for production; 3+ query variants rarely improve recall enough to justify cost
- Always set `similarity_cutoff` on `SimilarityPostprocessor` before passing to cross-encoder reranker; pre-filtering reduces reranking time by 50-80%
- Use `SubQuestionQueryEngine` only for genuinely multi-source queries; for single-source with complex phrasing, query expansion in `QueryFusionRetriever` is sufficient and cheaper
- Pre-build evaluation datasets from real user queries with `generate_question_context_pairs()` — synthetic evaluation on your actual data beats generic benchmarks
- For `NLSQLTableQueryEngine`, restrict `include_tables` to only relevant tables — giving all tables increases SQL generation errors and cost
- Use `response_mode="tree_summarize"` for multi-document synthesis; "compact" truncates context silently which breaks faithfulness on long results
- Store persistent indexes with version tags (timestamp or content hash) so agents can load a specific snapshot and evaluation can be reproduced

## AI-agent gotchas
- `SubQuestionQueryEngine.query()` is synchronous; for async agent loops use `aquery()` or the agent will block the event loop
- `QueryFusionRetriever` with `use_async=True` opens many concurrent LLM calls; set a semaphore or use `asyncio.Semaphore` wrapper if hitting rate limits
- `NLSQLTableQueryEngine` does not sanitize SQL — an adversarial query can cause destructive SQL if the DB user has write permissions; always use a read-only database connection
- `PairwiseComparisonEvaluator` with `enforce_consistency=True` doubles the LLM calls (A-vs-B and B-vs-A) — disable for bulk evaluation
- `ReActAgent` in LlamaIndex does not automatically fall back when a tool returns an error; add explicit error handling in the tool function and return a structured error string
- Hierarchical index with `AutoMergingRetriever` fails silently if parent nodes were not created during ingestion — validate node relationships after parsing

## References
- https://docs.llamaindex.ai/en/stable/examples/retrievers/
- https://docs.llamaindex.ai/en/stable/examples/evaluation/
- https://docs.llamaindex.ai/en/stable/examples/query_engine/
- https://github.com/run-llama/llama_index/tree/main/docs/examples
- "Production RAG" — LlamaIndex blog: https://www.llamaindex.ai/blog
