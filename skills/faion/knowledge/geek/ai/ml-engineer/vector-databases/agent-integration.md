# Agent Integration — Vector Databases

## When to use
- Building a RAG pipeline that needs semantic similarity search
- Storing and querying document embeddings at scale (10K+ documents)
- Implementing multi-tenant knowledge bases with namespace isolation
- Replacing keyword-only search with semantic or hybrid search
- Benchmarking or migrating between vector DB providers

## When NOT to use
- Dataset fits in memory and has fewer than ~1,000 documents — use in-process numpy similarity instead
- Requirement is pure exact-match lookup — a relational DB or Redis suffices
- The application already uses Elasticsearch with kNN and a rewrite is not justified
- Prototyping a single-user tool with no persistence requirement — Chroma in-memory is enough

## Where it fails / limitations
- ANN (approximate nearest neighbor) does not guarantee finding the true nearest neighbor; Recall@10 is typically 90-99%, not 100%
- Quantization trades recall for memory savings; binary quantization loses 5-10% recall
- pgvector degrades significantly above ~10M vectors without sharding strategies
- Chroma is single-node only — not suitable for production multi-user workloads
- Pinecone vendor lock-in: no self-hosting option, filtering flexibility is limited compared to Qdrant
- Metadata filtering on unindexed fields causes full scans — always create payload indexes for filtered fields

## Agentic workflow
An agent receives a user query, embeds it using the configured embedding model, then calls the vector DB client to retrieve top-k semantically similar chunks. The agent can branch on score thresholds: if no result exceeds `score_threshold`, it rewrites the query or escalates to a web search tool. For multi-tenant SaaS, the agent injects the tenant namespace/collection before every query, preventing cross-tenant data leakage.

### Recommended subagents
- `faion-sdd-executor-agent` — orchestrates setup tasks (collection creation, index config, bulk upsert) from an implementation plan
- Custom retrieval subagent — wraps vector DB client + reranker; called by the main reasoning agent as a tool

### Prompt pattern
```
You are a retrieval agent. Given <query>, call the vector_search tool with:
- collection: "<namespace>"
- query_text: "<query>"
- top_k: 20
- score_threshold: 0.6
If fewer than 3 results are returned, rewrite the query by adding synonyms and retry once.
Return the top 5 results after applying the reranker.
```

```python
# Qdrant retrieval with score threshold
results = client.search(
    collection_name="docs",
    query_vector=embed(query),
    limit=20,
    score_threshold=0.6,
    query_filter=Filter(must=[FieldCondition(key="tenant_id", match=MatchValue(value=tenant))])
)
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `qdrant` (Docker) | Run Qdrant locally | `docker pull qdrant/qdrant` — [qdrant.tech/documentation](https://qdrant.tech/documentation/) |
| `qdrant-client` (Python) | Python SDK for Qdrant | `pip install qdrant-client` |
| `weaviate-client` (Python) | Python SDK for Weaviate | `pip install weaviate-client` |
| `pymilvus` | Python SDK for Milvus | `pip install pymilvus` |
| `pinecone` | Python SDK for Pinecone | `pip install pinecone` |
| `chromadb` | Embedded vector DB | `pip install chromadb` |
| `psycopg2` + `pgvector` | pgvector via PostgreSQL | `pip install pgvector psycopg2-binary` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Qdrant Cloud | SaaS + OSS | Yes — REST + gRPC | Free 1GB tier; Python/TS/Go SDKs |
| Pinecone | SaaS | Yes — REST SDK | Serverless billing; simple API; no self-host |
| Weaviate Cloud | SaaS + OSS | Yes — GraphQL + REST | Built-in hybrid search; text2vec modules |
| Milvus / Zilliz | OSS + SaaS | Yes — pymilvus | Best for 1B+ vectors; CNCF project |
| pgvector | OSS (PostgreSQL ext) | Yes — SQL/ORM | Familiar; ACID; degrades > 100M vectors |
| Chroma | OSS | Yes — Python | Local dev only; no production scale |
| Elasticsearch kNN | SaaS + OSS | Yes — REST | Good for existing ES infra; heavier footprint |

## Templates & scripts
See `templates.md` for collection setup, bulk upsert, and index configuration templates.

Inline: Qdrant collection setup with HNSW + scalar quantization (< 50 lines):

```python
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, HnswConfigDiff,
    ScalarQuantizationConfig, ScalarType, QuantizationConfig
)

client = QdrantClient("localhost", port=6333)

client.create_collection(
    collection_name="docs",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
    hnsw_config=HnswConfigDiff(m=16, ef_construct=200),
    quantization_config=QuantizationConfig(
        scalar=ScalarQuantizationConfig(type=ScalarType.INT8, always_ram=True)
    ),
)

# Create payload index for fast metadata filtering
client.create_payload_index(
    collection_name="docs",
    field_name="tenant_id",
    field_schema="keyword",
)
```

## Best practices
- Always create payload indexes on fields used in filters before bulk upsert, not after
- Use batch upserts of 100–500 points; single-point inserts are 10–50x slower at scale
- Enable scalar quantization (INT8) by default in production; only use binary quantization when memory is critical and 5-10% recall loss is acceptable
- Prefer gRPC over HTTP for Qdrant when inserting or querying at > 1,000 QPS
- Set `score_threshold` on queries to avoid injecting low-relevance chunks into LLM context
- For pgvector: always create HNSW index (not IVFFlat) for production; run `VACUUM ANALYZE` after bulk inserts; set `hnsw.ef_search` based on recall target
- Multi-tenancy: use Qdrant named collections per tenant for full isolation, or payload filtering for shared collections with strict index enforcement

## AI-agent gotchas
- Embedding model mismatch: if the model used at query time differs from ingestion time, similarity scores are meaningless — store model name as collection metadata and validate on startup
- Score threshold selection: a threshold that works for one query distribution may cause empty results for out-of-distribution queries; build a fallback (query expansion or web search)
- Stale index after bulk updates: Qdrant and Weaviate optimize indexes asynchronously; agent queries immediately after a large upsert may see degraded recall — add a ready-check before querying
- Human-in-loop checkpoint: before switching a production collection to binary quantization (32x compression, -5-10% recall), run an offline recall evaluation against your query set and require explicit approval
- Token budget: each retrieved chunk consumes LLM context; a top-k=20 query with 512-token chunks uses 10,240 tokens before the LLM generates anything — always pass through a reranker to reduce to top-5

## References
- [Qdrant documentation](https://qdrant.tech/documentation/)
- [ANN Benchmarks](https://ann-benchmarks.com/)
- [Qdrant Benchmarks](https://qdrant.tech/benchmarks/)
- [pgvector GitHub](https://github.com/pgvector/pgvector)
- [Weaviate Hybrid Search docs](https://weaviate.io/developers/weaviate/search/hybrid)
- [Pinecone Learning Center](https://www.pinecone.io/learn/)
- [ZenML Vector DB Comparison](https://www.zenml.io/blog/vector-databases-for-rag)
