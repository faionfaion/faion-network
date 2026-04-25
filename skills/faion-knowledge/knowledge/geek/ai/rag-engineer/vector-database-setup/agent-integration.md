# Agent Integration — Vector Database Setup

## When to use
- Starting a new RAG pipeline and need to choose and provision a vector store
- Migrating from one vector DB to another (e.g., Chroma → Qdrant for production)
- Building multi-tenant search where data isolation by namespace/collection is required
- Embedding datasets with >10K vectors where in-memory numpy arrays are no longer viable
- Recommendation or duplicate-detection systems needing fast ANN at scale

## When NOT to use
- Fewer than 5K vectors with no strict latency SLA — a simple numpy cosine search is sufficient and has zero infra overhead
- Relational data with complex JOINs where pgvector's SQL expressiveness is more valuable than ANN speed
- Text search where full BM25/TF-IDF ranking is the primary concern — dedicated Elasticsearch or Typesense is a better fit
- Throwaway experiments with no persistence requirement — in-memory Chroma is simpler

## Where it fails / limitations
- Dimension mismatch between the embedding model and collection definition causes silent upsert failures in some clients; always validate dimensions at ingestion time
- Distance metric choice (cosine vs L2 vs dot product) is irreversible without re-creating the collection — getting this wrong early is expensive
- Metadata (payload) stored in vector DBs has no referential integrity; stale or deleted source documents are not automatically removed from the index
- Without a metadata update strategy, document updates require delete+re-insert, and partial upserts (vector only, no payload) can leave payload out of sync
- HNSW index memory scales linearly with vector count; 10M × 1536-dim float32 vectors = ~60GB RAM before payload and overhead
- Cloud managed DBs (Pinecone Serverless) have cold-start latency on the first query after idle periods — not suitable for hard real-time SLAs

## Agentic workflow
An agent selects the appropriate vector store backend based on constraints (self-hosted vs managed, vector count estimate, filter complexity), provisions the collection with the correct schema and index type, then runs an ingestion loop. A second agent validates the setup by querying with known embeddings and asserting top-1 recall matches expected results. Schema selection and metric choice are human-confirmed before the collection is created.

### Recommended subagents
- `faion-sdd-executor-agent` — follows the implementation plan to provision, index, and validate the chosen vector store
- Custom evaluation agent — fires test queries post-ingest and checks precision@5 against a small labeled set

### Prompt pattern
```
You are a vector store provisioner. Given: provider (pinecone|chroma|qdrant|weaviate|pgvector),
vector_dim, distance_metric, filterable_fields, expected_vector_count.
Steps:
1. Select index type based on expected_vector_count (<10K→Flat, <1M→HNSW, >1M→IVF or HNSW+quantization).
2. Provision the collection/index.
3. Create indexes for each filterable_field.
4. Return: {"provider": "...", "collection": "...", "index_type": "...", "status": "ready"}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pinecone` (Python SDK) | Manage Pinecone indexes and upsert | `pip install pinecone` / [docs](https://docs.pinecone.io/) |
| `chromadb` | Local/persistent vector store | `pip install chromadb` / [docs](https://docs.trychroma.com/) |
| `qdrant-client` | Qdrant CRUD and search | `pip install qdrant-client` / [docs](https://python-client.qdrant.tech/) |
| `weaviate-client` | Weaviate v4 Python client | `pip install weaviate-client` / [docs](https://weaviate.io/developers/weaviate/client-libraries/python) |
| `pgvector` | PostgreSQL extension for vectors | `pip install pgvector` / [GitHub](https://github.com/pgvector/pgvector) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Pinecone | SaaS | Yes — REST + Python SDK | Serverless and pod-based; no infra; cold-start on serverless |
| Qdrant Cloud | SaaS | Yes — same client as OSS | Good for self-hosted-to-cloud migration |
| Weaviate Cloud | SaaS | Yes — Python/REST | Built-in vectorizer modules (OpenAI, Cohere) |
| Chroma OSS | OSS | Yes — local or client-server | Best for development; limited horizontal scaling |
| pgvector | OSS extension | Yes — standard SQL | Best when already on PostgreSQL; IVFFlat index |
| Milvus | OSS | Yes — pymilvus | Enterprise scale; Kubernetes-native |

## Templates & scripts
See `templates.md` for VectorStoreBase abstract class and factory pattern.

Key pattern: always wrap the chosen vector store behind the `VectorStoreBase` interface so the agent can swap backends without changing upstream RAG code:

```python
class VectorStoreFactory:
    @staticmethod
    def create(provider: str, **kwargs):
        if provider == "qdrant":
            return QdrantStore(**kwargs)
        elif provider == "chroma":
            return ChromaStore(**kwargs)
        elif provider == "pinecone":
            return PineconeStore(**kwargs)
        raise ValueError(f"Unknown provider: {provider}")
```

## Best practices
- Validate embedding dimension against collection config at startup — raise early rather than silently upsert wrong-dim vectors
- Choose HNSW for latency-sensitive production search; IVF only if RAM is the binding constraint
- Store raw text content in metadata/payload alongside the embedding — agents need to return human-readable context, not just IDs
- Keep metadata fields small (KB scale); store large blobs in S3/GCS and put only the object key in metadata
- Use consistent, deterministic IDs derived from document hash so re-ingestion is idempotent (upsert, not insert)
- Test distance metric choice with a 100-sample labeled set before committing to a schema
- For multi-tenant apps, use separate namespaces (Pinecone) or collections (Qdrant/Chroma) per tenant rather than metadata filtering — prevents cross-tenant data leaks

## AI-agent gotchas
- Agents should never call `delete_collection` without human confirmation — there is no undo
- Collection creation is not idempotent in all clients; wrap in try/except and check for "already exists" errors rather than blind re-create
- Pinecone Serverless has per-request limits (100 vectors/upsert, 10K vectors/query result); agents must chunk accordingly
- Embedding model changes (e.g., switching from `text-embedding-3-small` to `text-embedding-3-large`) require full re-ingestion — agents must detect dimension mismatch and trigger a rebuild workflow, not just upsert on top
- Chroma's persistent client is not safe for concurrent multi-process writes — use the client-server mode in multi-agent deployments
- pgvector IVFFlat index requires `VACUUM ANALYZE` after bulk inserts for the planner to use the index; agents running bulk loads must include this step

## References
- [Pinecone Docs](https://docs.pinecone.io/)
- [Chroma Docs](https://docs.trychroma.com/)
- [Qdrant Docs](https://qdrant.tech/documentation/)
- [Weaviate Docs](https://weaviate.io/developers/weaviate)
- [pgvector GitHub](https://github.com/pgvector/pgvector)
- [ANN Benchmarks](https://ann-benchmarks.com/)
- [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)
