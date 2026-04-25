# Agent Integration — Chroma Vector Database

## When to use
- Local development and prototyping of RAG pipelines (no external server needed)
- Single-developer projects or small teams where operational simplicity trumps scale
- Running evaluation harnesses in CI where spinning up Qdrant/Weaviate adds friction
- Notebook-based research and experimentation with embeddings
- Applications that need an embedded vector store with zero infrastructure (similar role to SQLite)

## When NOT to use
- Production deployments with >1M vectors — Chroma performance degrades and lacks the tuning options of Qdrant/Weaviate
- Multi-tenant SaaS applications — Chroma has no native access control or tenant isolation
- High-concurrency write workloads — PersistentClient uses SQLite under the hood; write throughput is limited
- You need ANN index tuning (HNSW ef_construction, m parameters) — Chroma exposes limited knobs vs. Qdrant
- Multi-node horizontal scaling — Chroma does not support distributed deployment

## Where it fails / limitations
- `chromadb.Client()` (in-memory) loses all data on process exit; agents that restart mid-pipeline lose the index
- `PersistentClient` uses SQLite; concurrent writes from multiple processes/workers corrupt the database
- Metadata filter syntax (`where`, `where_document`) supports only a subset of operators; complex nested filters are not supported
- IDs must be strings; agents using integer IDs must stringify them explicitly
- Distance metric (`cosine`, `l2`, `ip`) must be set at collection creation and cannot be changed — migrations require full collection recreation
- Collection query returns distances, not similarity scores; for cosine space, `similarity = 1 - distance`

## Agentic workflow
An ingestion subagent creates or loads a persistent Chroma collection, upserts chunks in batches of 500 (Chroma performs best with batch sizes 100-1000), and emits a completion summary with collection stats. A retrieval subagent calls `collection.query()` with the query embedding and metadata filters, transforms the distance scores to similarities, and returns ranked results. Both subagents use `get_or_create_collection` so re-runs are idempotent. No human review needed for Chroma in development; flag to review before promoting to production if usage exceeds 500k vectors.

### Recommended subagents
- `faion-sdd-executor-agent` — implement the Chroma integration as a task in a RAG ingestion pipeline

### Prompt pattern
```
Initialize or load Chroma collection "{{collection_name}}" with cosine similarity.
Upsert the following chunks (JSON list of {id, text, embedding, metadata}).
Return: total vectors in collection, upsert duration, any failed IDs.

Collection path: {{persist_path}}
Chunks: {{chunks_json}}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `chromadb` | Core client library (embedded + HTTP client modes) | `pip install chromadb` · https://docs.trychroma.com |
| `langchain-chroma` | LangChain VectorStore wrapper for Chroma | `pip install langchain-chroma` · https://python.langchain.com/docs/integrations/vectorstores/chroma |
| `llama-index-vector-stores-chroma` | LlamaIndex Chroma vector store | `pip install llama-index-vector-stores-chroma` |
| `chroma` (Docker) | Chroma HTTP server for multi-process access | `docker pull chromadb/chroma` · https://docs.trychroma.com/production/containers/docker |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Chroma (embedded) | OSS | Yes (Python in-process) | Zero infra; ideal for dev/test/CI |
| Chroma (Docker server) | OSS | Yes (HTTP REST) | Enables multi-process access; still single-node |
| Chroma Cloud | SaaS (beta) | Yes (REST) | Managed Chroma; not yet GA as of 2026 |

## Templates & scripts
See `templates.md` for basic Chroma usage and LangChain integration templates.

Inline — idempotent upsert helper with batch chunking:
```python
import chromadb

def upsert_chunks(
    chunks: list[dict],
    collection_name: str,
    persist_path: str = "./chroma_db",
    batch_size: int = 500,
) -> dict:
    client = chromadb.PersistentClient(path=persist_path)
    col = client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"},
    )
    total = 0
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i+batch_size]
        col.upsert(
            ids=[c["id"] for c in batch],
            embeddings=[c["embedding"] for c in batch],
            metadatas=[c.get("metadata", {}) for c in batch],
            documents=[c["text"] for c in batch],
        )
        total += len(batch)
    return {"collection": collection_name, "upserted": total, "total": col.count()}
```

## Best practices
- Always use `PersistentClient` with an explicit `path`; in-memory client data loss is the most common Chroma mistake in agent pipelines
- Set `metadata={"hnsw:space": "cosine"}` at collection creation — the default `l2` is wrong for normalized embeddings
- Use `get_or_create_collection` (not `create_collection`) so agent re-runs are idempotent and don't fail on duplicate collection names
- Batch upserts in chunks of 500; single large upserts (>5000 items) can hit SQLite WAL limits
- Store `source`, `chunk_index`, and `created_at` in metadata by default — these are the minimum fields needed for citation and freshness filtering
- For CI/evaluation pipelines, use in-memory client with a fixture that pre-seeds the collection; persistent client in CI creates state leakage between test runs

## AI-agent gotchas
- Chroma's `where` filter requires all metadata keys to be present on the document; filtering on a key that some documents lack silently excludes those documents from results
- `collection.query()` returns a dict of lists, not a list of dicts; agents that expect `results[0]["id"]` will get a `KeyError` — access as `results["ids"][0][0]`
- Distance values in cosine space are in `[0, 2]`, not `[0, 1]`; `similarity = 1 - distance` is the correct conversion
- `PersistentClient` creates a `.chroma` directory and SQLite file at `path`; agents writing to a read-only filesystem will silently fail to persist
- LangChain's `Chroma.from_documents()` creates a new collection each call if `collection_name` is not set; agents calling it in a loop will create N duplicate collections

## References
- https://docs.trychroma.com/
- https://github.com/chroma-core/chroma
- https://python.langchain.com/docs/integrations/vectorstores/chroma
- https://docs.trychroma.com/production/containers/docker
