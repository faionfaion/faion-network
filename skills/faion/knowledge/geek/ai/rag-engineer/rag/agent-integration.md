# Agent Integration — RAG Pipeline

## When to use
- Agent needs to answer questions grounded in a private or frequently-updated document corpus.
- Reducing hallucinations on domain-specific topics not in the model's training data.
- Building a knowledge assistant over PDFs, docs, wikis, or code repositories.
- When the source corpus is too large to fit in a single context window.
- Citation / source attribution is required for compliance or user trust.

## When NOT to use
- Document set is tiny (< 50 chunks) and fits in context — just stuff the full context.
- Questions are purely general knowledge; RAG adds retrieval latency with no accuracy gain.
- Real-time data (stock prices, live APIs) — RAG retrieves static indexed content; use live tool calls instead.
- Query volume is very low and latency is critical — the embed + retrieve round-trip adds 200–600ms.

## Where it fails / limitations
- Retrieval quality is bounded by chunk quality; bad chunking = bad results regardless of generation model.
- Semantic search fails for exact technical terms, product codes, or rare names — use hybrid search.
- Faithfulness scores degrade when retrieved context partially contradicts itself (conflicting document versions).
- Reranking adds 100–300ms latency; skip for latency-critical applications.
- Index goes stale without incremental update pipelines — answers reference outdated information.
- `top_k=10` retrieval with `response_mode=compact` can exceed context limits for large chunks — always bound `top_k * chunk_size`.

## Agentic workflow
A retrieval subagent receives the user query, embeds it, and fetches top-k chunks from the vector store. A reranker subagent scores the chunks and selects the top 5 most relevant. A generation subagent synthesizes the answer using the reranked context with a strict "answer only from context" prompt. A citation subagent extracts source references from the generation output and validates them against the retrieved chunk metadata. The orchestrator assembles the final response with citations.

### Recommended subagents
- `query-embedder` — Embeds the user query and calls the vector store retrieval API.
- `reranker` — Scores retrieved chunks with a cross-encoder; returns top N.
- `rag-generator` — Synthesizes answer from reranked context; enforces "only use provided context" constraint.
- `citation-extractor` — Parses source references from generated text and validates against chunk metadata.

### Prompt pattern
```xml
<system>
You are a knowledge assistant. Answer ONLY from the provided context below.
If the context does not contain enough information, say "I don't have that in my knowledge base."
Always cite sources as [Source: {filename}, page {page}].
</system>
<context>
{retrieved_chunks}
</context>
```

Retrieval call (LlamaIndex):
```python
query_engine = index.as_query_engine(
    similarity_top_k=20,
    node_postprocessors=[reranker],  # Rerank to top 5
    response_mode="compact",
    text_qa_template=qa_prompt,
)
response = query_engine.query(user_query)
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `llama-index` | End-to-end RAG: load, chunk, embed, query | `pip install llama-index` / docs.llamaindex.ai |
| `langchain` | RAG chains, retrievers, document loaders | `pip install langchain` / python.langchain.com |
| `ragas` | RAG evaluation: faithfulness, answer relevance, context recall | `pip install ragas` / docs.ragas.io |
| `qdrant-client` | Python client for Qdrant vector DB | `pip install qdrant-client` / qdrant.tech |
| `unstructured` | Parse PDFs, DOCX, HTML to clean text | `pip install unstructured` / unstructured.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Qdrant | OSS / Cloud | Yes | Recommended production vector DB; payload filtering |
| Chroma | OSS | Yes | Dev/prototyping; in-memory or local persistent |
| LlamaCloud | SaaS | Yes | Managed parsing + indexing; LlamaIndex hosted |
| Pinecone | SaaS | Yes | Fully managed; serverless tier; good for 1B+ vectors |
| Cohere Rerank | SaaS | Yes | Best-in-class reranking API; `rerank-3` model |
| OpenAI Embeddings | SaaS | Yes | `text-embedding-3-large` (3072-dim) standard choice |
| Voyage AI | SaaS | Yes | `voyage-3` — strong alternative to OpenAI embeddings |

## Templates & scripts
See `templates.md` for full build/query/evaluate pipeline templates.

Minimal RAG query with reranking:
```python
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.core.postprocessor import SentenceTransformerRerank

storage = StorageContext.from_defaults(persist_dir="./index")
index = load_index_from_storage(storage)
reranker = SentenceTransformerRerank(
    model="cross-encoder/ms-marco-MiniLM-L-2-v2", top_n=5
)
engine = index.as_query_engine(similarity_top_k=20, node_postprocessors=[reranker])
response = engine.query("your question here")
print(response.response)
for node in response.source_nodes:
    print(f"[{node.score:.2f}] {node.metadata.get('file_name')} — {node.text[:100]}")
```

## Best practices
- Test chunk size empirically: 512 tokens for Q&A, 1024 for technical docs, 1500 for research papers.
- Always add metadata (source filename, page, section, date) at index time — it's impossible to add retroactively without re-indexing.
- Use hybrid search (BM25 + vector) by default; fall back to pure vector only after benchmarking shows no improvement.
- Evaluate retrieval quality with RAGAS before launching; aim for MRR > 0.7, faithfulness > 0.9.
- Cache frequent queries at the application layer — same query string → same retrieval result.
- Implement incremental indexing: track document hashes, re-index only changed documents.
- Deduplicate near-identical chunks before indexing (cosine similarity > 0.97) to avoid redundant context.

## AI-agent gotchas
- Retrieved context order matters: put highest-scored chunks first in the prompt (models attend better to earlier content).
- Agents may silently ignore `"answer only from context"` constraints — add an explicit faithfulness check as a post-generation step.
- If the query requires combining facts from more than 3 separate chunks, standard RAG degrades; switch to agentic RAG with iterative retrieval.
- Index re-embedding after changing the embedding model requires complete re-indexing — plan for downtime or blue/green index strategy.
- Token budget: `top_k * avg_chunk_tokens` must stay well below the model's context limit after adding system prompt and few-shot examples.
- Human-in-loop checkpoint: when faithfulness score < 0.8 on production queries, queue them for human review rather than surfacing the answer to users.

## References
- https://docs.llamaindex.ai/ — LlamaIndex documentation
- https://docs.ragas.io/en/latest/ — RAGAS evaluation framework
- https://qdrant.tech/documentation/ — Qdrant vector database
- https://arxiv.org/abs/2005.11401 — RAG: Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (original paper)
- https://python.langchain.com/docs/tutorials/rag/ — LangChain RAG tutorial
