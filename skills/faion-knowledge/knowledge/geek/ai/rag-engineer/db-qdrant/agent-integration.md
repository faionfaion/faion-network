# Agent Integration — Qdrant Vector Database

## When to use
- Standing up a production self-hosted vector store (Docker or Kubernetes)
- RAG pipelines needing payload-level filtering alongside vector similarity
- Systems requiring hybrid dense+sparse (BM25) search without a separate search engine
- High-volume indexing (>1M vectors) with memory constraints — scalar/binary quantization cuts RAM 4-32x
- Multi-modal retrieval where one point stores both text and image vectors as named vectors
- Pipelines that need point-level snapshots and incremental backups without downtime

## When NOT to use
- Prototype/local dev with <50K vectors and no filtering needs — Chroma is simpler and zero-config
- Existing PostgreSQL stack where pgvector extension is already available
- Teams that need a fully managed SaaS with zero infra ops — Pinecone or Qdrant Cloud are better fits
- Requirements for GraphQL or Weaviate-style schema-first data modeling

## Where it fails / limitations
- gRPC port (6334) must be explicitly opened; forgetting it causes silent REST-only mode with 2-3x lower throughput
- Sparse vector (BM25) setup requires pre-tokenization outside Qdrant — the DB stores indices/values, not raw text
- HNSW index build is memory-intensive; `indexing_threshold` must be tuned or bulk-load will OOM on small machines
- Payload index creation is synchronous and can stall searches on large collections during index build
- Snapshot restore requires correct collection to be absent first; restoring over existing collection fails silently
- Binary quantization degrades recall for low-dimensional embeddings (<256 dims) significantly

## Agentic workflow
A Claude subagent provisions a Qdrant collection, ingests documents in batches of 100, and creates payload indexes for any metadata fields used in filters. Retrieval agents call the search endpoint with `query_filter` composed from structured metadata to narrow the ANN search. A separate maintenance agent runs nightly snapshots and optionally triggers quantization updates when the collection exceeds a size threshold.

### Recommended subagents
- `faion-sdd-executor-agent` — executes the implementation plan steps for collection schema, index config, and quantization settings
- Custom ingestion agent — batches embed+upsert cycles with retry on rate-limit errors

### Prompt pattern
```
You are a Qdrant setup agent. Given: collection_name, vector_size, distance_metric, payload_schema.
Steps:
1. Create collection with HNSW config (m=16, ef_construct=100).
2. Create payload indexes for each filterable field.
3. Return: {"collection": "<name>", "status": "ready", "indexed_fields": [...]}
```

```
You are a batch ingestor. Given: list of {id, text, metadata}.
For each batch of 100:
1. Call embed API, attach vectors.
2. Upsert to Qdrant.
3. On error: log and skip, do not halt.
Return: {"total_upserted": N, "failed": M}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `qdrant-client` (Python) | Full CRUD + search + admin | `pip install qdrant-client` / [docs](https://python-client.qdrant.tech/) |
| `qdrant` Docker image | Self-hosted server | `docker pull qdrant/qdrant` / [docs](https://qdrant.tech/documentation/guides/installation/) |
| REST API (curl/httpie) | Inspection and ad-hoc ops | Port 6333 / [OpenAPI](https://qdrant.github.io/qdrant/redoc/index.html) |
| gRPC (port 6334) | High-throughput production | `prefer_grpc=True` in client config |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Qdrant Cloud | SaaS | Yes — same Python client, just add `api_key` | Managed, auto-scale clusters |
| Qdrant OSS (Docker) | OSS | Yes — REST + gRPC | Recommended for self-hosted prod |
| LangChain Qdrant integration | OSS wrapper | Yes — `QdrantVectorStore` | Drop-in for LangChain RAG chains |
| LlamaIndex Qdrant integration | OSS wrapper | Yes — `QdrantVectorStore` | Works with LlamaIndex query engines |

## Templates & scripts
See `templates.md` for collection provisioning and batch upsert templates.

Inline: 40-line batch ingestor with retry:
```python
import time
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

def batch_upsert(client: QdrantClient, collection: str, points: list, batch=100, retries=3):
    for i in range(0, len(points), batch):
        chunk = points[i:i+batch]
        for attempt in range(retries):
            try:
                client.upsert(collection_name=collection, points=chunk)
                break
            except Exception as e:
                if attempt == retries - 1:
                    raise
                time.sleep(2 ** attempt)
```

## Best practices
- Always set `on_disk_payload=True` for collections storing large text payloads; keeps vectors in RAM while payloads hit disk
- Use `prefer_grpc=True` with timeout=30 in production clients — gRPC throughput is 2-3x REST
- Create payload indexes before bulk ingestion, not after — adding indexes post-ingest locks the collection
- Set `indexing_threshold` to 0 during bulk load, then restore to 20000 after — avoids repeated HNSW rebuilds
- Use `with_vectors=False` in search responses unless the caller explicitly needs raw vectors — reduces response size 5-10x
- Enable binary quantization with `always_ram=True` and `rescore=True` + `oversampling=2.0` for balanced speed/recall
- Use UUIDs or deterministic integer IDs for points; random IDs cause HNSW locality degradation at scale

## AI-agent gotchas
- Agents must check `info.indexed_vectors_count` vs `info.points_count` before querying — unindexed points are searched with brute force and skew latency benchmarks
- Sparse vector construction (BM25 token IDs + weights) must happen in the agent's pre-processing step, not inside Qdrant — agents need a tokenizer (e.g., `fastembed` or custom BM25Encoder)
- Score thresholds (`score_threshold=0.7`) silently return zero results if embeddings are not normalized — agents should validate that embedding magnitudes are ~1.0 for cosine distance
- Snapshot restore requires the agent to DELETE the collection first — this is a destructive step that needs human-in-loop confirmation in production
- Agent loops that call `create_collection` on every startup will fail if the collection exists — always guard with `get_collection` + exception handling
- Quantization `always_ram=True` requires that RAM >= collection vector footprint; agent must query `info.vectors_size_bytes` and compare against host memory before enabling

## References
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Qdrant Python Client](https://github.com/qdrant/qdrant-client)
- [Hybrid Search Guide](https://qdrant.tech/articles/hybrid-search/)
- [Quantization Guide](https://qdrant.tech/documentation/guides/quantization/)
- [Qdrant Cloud](https://qdrant.tech/documentation/cloud/)
