# Agent Integration — RAG Pipeline Design

## When to use
- LLM needs access to private, domain-specific, or frequently updated knowledge not in training data
- Application requires citations: users need to verify sources for trust
- Knowledge base exceeds the model's context window (>200K tokens of documents)
- Multiple heterogeneous data sources (PDFs, SQL DB, APIs) need unified semantic search
- Answer accuracy on domain queries is below acceptable threshold with prompt engineering alone

## When NOT to use
- Knowledge is fully covered by the model's training and does not change — prompt engineering suffices
- Retrieval latency >500ms is unacceptable and caching cannot compensate (e.g., real-time trading)
- Corpus is <50 documents — just include them all in the context window (simpler, often more accurate)
- Team lacks infra to maintain a vector database and embedding pipeline — use a managed RAG service (LlamaCloud, Azure AI Search)
- Queries are always the same — pre-generate answers and cache them instead of building a full pipeline

## Where it fails / limitations
- Naive chunking (fixed-size split) loses cross-sentence semantic boundaries — accuracy 10-20% below semantic chunking
- Retrieval recall@10 >85% is achievable but requires hybrid search (vector + BM25) — pure vector search alone misses exact-match queries
- Hallucination is not eliminated by RAG — the LLM can still confabulate when retrieved context is ambiguous or irrelevant
- GraphRAG (entity extraction) costs 5-10x more at indexing time and requires accurate NER — do not use for general knowledge bases
- Embedding model lock-in: re-indexing the entire corpus is required when switching embedding models
- Cold start: first query after index build returns stale embeddings if documents changed during build
- Multi-tenant isolation in shared vector DBs requires careful namespace/collection partitioning — data leakage risk

## Agentic workflow
RAG fits naturally as a tool in an agentic loop. The orchestrator calls a `search_knowledge_base(query, top_k=5)` tool, receives ranked passages with source metadata, and uses them to synthesize a grounded response. For complex queries, use Agentic RAG: the agent reformulates the query if initial results are insufficient, applies metadata filters (date range, source type), and iterates retrieval up to 3 times before answering. Multi-agent setups can dispatch parallel retrieval agents over different corpora (vector DB, SQL, web search) and merge results at the synthesis stage.

### Recommended subagents
- `faion-sdd-executor-agent` — can be given a search tool backed by a RAG pipeline to answer research questions within SDD workflows

### Prompt pattern
```xml
<tools>
  <tool name="search_knowledge_base">
    <description>
      Semantic search over company documentation. Returns top-K passages with source citations.
      Use this before answering any factual question about company policies, products, or procedures.
    </description>
    <parameters>
      {
        "query": "string — natural language search query",
        "top_k": "integer — number of results (default 5, max 10)",
        "source_filter": "optional string — filter by document source (e.g. 'contracts', 'policies')"
      }
    </parameters>
  </tool>
</tools>
<task>
  Answer the user's question. Always call search_knowledge_base first.
  Cite your sources using the document titles returned.
  If search results are insufficient, say so — do not guess.
</task>
```

```python
# Agentic RAG loop (simplified)
MAX_RETRIEVAL_ROUNDS = 3
for round_num in range(MAX_RETRIEVAL_ROUNDS):
    results = vector_db.search(query=reformulated_query, top_k=5)
    if is_sufficient(results, quality_threshold=0.7):
        break
    reformulated_query = llm.reformulate(original_query, previous_results=results)
answer = llm.synthesize(original_query, context=results)
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `qdrant-client` | Qdrant vector DB Python client | `pip install qdrant-client` / [docs](https://qdrant.tech/documentation/) |
| `langchain` | RAG pipeline orchestration | `pip install langchain langchain-community` / [docs](https://python.langchain.com/) |
| `llama-index` | Document-centric RAG framework | `pip install llama-index` / [docs](https://docs.llamaindex.ai/) |
| `sentence-transformers` | Local embedding models | `pip install sentence-transformers` / [docs](https://sbert.net/) |
| `ragas` | RAG evaluation (faithfulness, relevancy, recall) | `pip install ragas` / [docs](https://docs.ragas.io/) |
| `rank-bm25` | BM25 keyword search for hybrid retrieval | `pip install rank-bm25` |
| `unstructured` | PDF, DOCX, HTML parsing for ingestion | `pip install unstructured[all-docs]` / [docs](https://docs.unstructured.io/) |
| `pgvector` | Vector extension for PostgreSQL | `pip install pgvector` / [github](https://github.com/pgvector/pgvector) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Qdrant | OSS + SaaS | Yes | Best self-hosted; Rust perf; hybrid search built-in; rich filtering |
| Pinecone | SaaS | Yes | Managed, serverless; auto-scaling; 40KB metadata/vector |
| Weaviate | OSS + SaaS | Yes | GraphQL API; hybrid search; knowledge graph modules |
| Chroma | OSS | Yes | Local dev only; simple API; not for multi-process prod |
| pgvector | OSS (Postgres ext) | Yes | No new infra if Postgres exists; limited to 2000 dims |
| Azure AI Search | SaaS | Yes | Enterprise; hybrid search + semantic ranking built-in |
| LlamaCloud | SaaS | Yes | Managed RAG pipeline; LlamaParse included |
| Cohere Embed | SaaS | Yes | Embed-v3 tops MTEB; multilingual; reranker API |
| Voyage AI | SaaS | Yes | voyage-3-large outperforms OpenAI by 9-20% on retrieval |

## Templates & scripts
```python
# rag_pipeline.py — production RAG with hybrid search + reranking (≤50 lines)
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from openai import OpenAI
import uuid

openai = OpenAI()
qdrant = QdrantClient(url="http://localhost:6333")
COLLECTION = "knowledge_base"
EMBED_MODEL = "text-embedding-3-small"
EMBED_DIM = 1536

def embed(text: str) -> list[float]:
    return openai.embeddings.create(input=text, model=EMBED_MODEL).data[0].embedding

def ingest(docs: list[dict]) -> None:
    """docs: [{"text": "...", "source": "...", "title": "..."}]"""
    qdrant.recreate_collection(COLLECTION, vectors_config=VectorParams(size=EMBED_DIM, distance=Distance.COSINE))
    points = [
        PointStruct(id=str(uuid.uuid4()), vector=embed(d["text"]), payload=d)
        for d in docs
    ]
    qdrant.upsert(collection_name=COLLECTION, points=points)

def search(query: str, top_k: int = 5, source_filter: str = None) -> list[dict]:
    query_filter = None
    if source_filter:
        from qdrant_client.models import Filter, FieldCondition, MatchValue
        query_filter = Filter(must=[FieldCondition(key="source", match=MatchValue(value=source_filter))])
    results = qdrant.search(
        collection_name=COLLECTION,
        query_vector=embed(query),
        limit=top_k,
        query_filter=query_filter,
        with_payload=True,
    )
    return [{"text": r.payload["text"], "source": r.payload["source"], "score": r.score} for r in results]
```

## Best practices
- Use hybrid search (vector + BM25) as the default — improves recall@10 by 15-25% over pure vector search
- Chunk size 400-512 tokens with 50-token overlap is a reliable default; tune based on document type
- Add source metadata at ingestion: `{"source": "policy/refunds", "date": "2026-01"}` — enables date-range filtering
- Rerank retrieved passages with Cohere Rerank or BGE Reranker before synthesis — top-5 after reranking > top-20 without it
- Evaluate the pipeline before deploying: run `ragas` on 50-100 labeled QA pairs to measure faithfulness and relevancy
- Cache embeddings for documents — embedding is expensive; hash document content and skip re-embedding unchanged docs
- Use `parent-child` chunking: embed small child nodes (200 tokens), return parent chunk (1000 tokens) for synthesis
- Monitor retrieval score distribution in production: score drift indicates embedding model mismatch or data drift

## AI-agent gotchas
- Retrieved context is injected verbatim into the LLM prompt — long chunks eat context budget fast; compress or truncate before injection
- LLMs treat all retrieved passages with equal weight; add explicit instructions ("Prioritize passages with score >0.85") or re-rank before passing
- Stale embeddings after document updates cause retrieval to return outdated content; implement incremental re-indexing triggered by document change events
- Multi-tenant RAG must isolate namespaces strictly — a missing filter parameter causes data leakage across tenants
- HyDE (Hypothetical Document Embedding) improves recall for technical queries but adds an LLM call per query — budget for the extra latency and cost
- Agentic retrieval loops can get stuck reformulating the same failing query; add a "no results" threshold and escalate to the user
- Embedding model dimension changes (e.g., 1536 → 3072) require full re-indexing — plan for this in the migration path

## References
- [RAG Architecture Explained 2025 — orq.ai](https://orq.ai/blog/rag-architecture)
- [Azure RAG Solution Design Guide](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-solution-design-and-evaluation-guide)
- [Ragas Evaluation Framework](https://docs.ragas.io/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Voyage AI Embeddings](https://docs.voyageai.com/)
- [Cohere Rerank API](https://docs.cohere.com/docs/rerank-2)
- [Best Chunking Strategies 2025 — Firecrawl](https://www.firecrawl.dev/blog/best-chunking-strategies-rag-2025)
- [RAG in Production — Coralogix](https://coralogix.com/ai-blog/rag-in-production-deployment-strategies-and-practical-considerations/)
