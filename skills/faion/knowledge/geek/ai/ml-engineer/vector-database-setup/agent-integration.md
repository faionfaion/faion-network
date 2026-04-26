# Agent Integration — Vector Database Setup

## When to use
- Setting up a new RAG pipeline that needs persistent vector storage beyond in-memory prototyping
- Migrating from Chroma (dev) to a production-grade database (Qdrant, Weaviate, Milvus)
- Scaling an existing vector store past 1M vectors where single-node setup hits memory or latency limits
- Adding vector search to an existing PostgreSQL stack via pgvector extension
- Compliance or data-sovereignty constraints require self-hosted deployment

## When NOT to use
- Proof-of-concept with < 10K documents — use Chroma in-memory or pgvector on existing Postgres
- Fully managed RAG without ops budget — use Pinecone Serverless or Weaviate Cloud directly; no setup needed
- The bottleneck is embedding quality or chunking strategy, not the database — fix those first

## Where it fails / limitations
- HNSW index build time is O(n log n) — initial indexing of 10M+ vectors takes hours and blocks queries
- Qdrant scalar quantization reduces memory 4x but introduces 1–2% recall loss; agents must account for this in quality targets
- pgvector HNSW index does not support online updates without re-indexing; high-write workloads degrade index quality
- Weaviate multi-node cluster setup requires etcd; ops complexity spikes significantly
- Milvus requires MinIO + etcd as dependencies — Docker Compose works locally but Kubernetes is needed for production HA
- Cloud-managed costs scale super-linearly with vector count and query volume — model cost at scale before committing

## Agentic workflow
An agent handles vector DB setup as a one-time infrastructure task: it reads the target DB selection from config, provisions the service (Docker or managed API), creates the schema/collection, and verifies the connection. For ongoing operations agents call upsert/search APIs directly. The setup agent outputs a validated connection config that downstream RAG agents consume. Infrastructure changes (index parameter tuning, quantization toggles) should go through a separate agent invocation with a dry-run step.

### Recommended subagents
- `faion-sdd-executor-agent` — when vector DB setup is a tracked SDD task with checklist and rollback plan
- General Claude subagent with shell/Python tools — for interactive provisioning and validation

### Prompt pattern
```
Set up a Qdrant collection named "{collection_name}" with:
- Dimensions: {dim}
- Distance: cosine
- Scalar quantization: int8
- HNSW m=16, ef_construct=100

1. Verify Qdrant is running at {host}:{port}
2. Create collection if it does not exist
3. Return collection info JSON
```

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, ScalarQuantizationConfig, ScalarType

client = QdrantClient(host="localhost", port=6333)
client.recreate_collection(
    collection_name="docs",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
    quantization_config=ScalarQuantizationConfig(
        type=ScalarType.INT8, quantile=0.99, always_ram=True
    ),
)
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `qdrant-client` | Python client for Qdrant REST/gRPC | `pip install qdrant-client` · qdrant.tech/documentation |
| `weaviate-client` | Python/JS client for Weaviate | `pip install weaviate-client` · weaviate.io/developers |
| `pymilvus` | Python client for Milvus | `pip install pymilvus` · milvus.io/docs |
| `pgvector` | PostgreSQL extension | `CREATE EXTENSION vector;` · github.com/pgvector/pgvector |
| `pinecone` | Pinecone Python client | `pip install pinecone` · docs.pinecone.io |
| `chromadb` | Chroma client (dev/proto) | `pip install chromadb` · docs.trychroma.com |
| `docker` / `docker compose` | Local DB provisioning | docker.com/get-docker |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Qdrant Cloud | SaaS | Yes — same client as OSS | Free tier 1GB; REST + gRPC; no infra |
| Weaviate Cloud | SaaS | Yes — REST/GraphQL | Free sandbox; managed HA |
| Zilliz Cloud | SaaS | Yes — pymilvus compatible | Managed Milvus; free tier |
| Pinecone Serverless | SaaS | Yes — REST + client | Pay-per-query; best managed option |
| Supabase (pgvector) | SaaS | Yes — PostgreSQL connection | Free tier; pgvector pre-installed |
| Neon (pgvector) | SaaS | Yes — PostgreSQL connection | Serverless Postgres; pgvector support |
| Qdrant OSS | OSS | Yes — Docker | Self-hosted; best OSS choice for production |

## Templates & scripts
See `templates.md` for Docker Compose files for Qdrant, Weaviate, and Milvus standalone.

Inline: production-ready Qdrant Docker Compose (< 30 lines):

```yaml
# docker-compose.qdrant.yml
services:
  qdrant:
    image: qdrant/qdrant:latest
    restart: unless-stopped
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_storage:/qdrant/storage
      - ./qdrant_config.yaml:/qdrant/config/production.yaml
    environment:
      QDRANT__SERVICE__API_KEY: "${QDRANT_API_KEY}"
      QDRANT__TLS__ENABLED: "false"

volumes:
  qdrant_storage:
```

## Best practices
- Start with scalar quantization (int8) enabled from day one — switching later requires full re-indexing
- Use gRPC (port 6334) instead of REST for bulk upserts — 2–4x throughput improvement
- Set `always_ram: true` for quantized vectors to keep the index hot; move raw vectors to disk if memory-constrained
- Create collections with `on_disk_payload: true` if metadata is large but search is vector-only
- For pgvector: always build HNSW index (not IVFFlat) for production; set `maintenance_work_mem = '1GB'` during index build
- Monitor `disk_usage` and `ram_usage` per collection — Qdrant exposes these via `/collections/{name}` endpoint
- Use namespaces (Pinecone) or tenants (Qdrant) for multi-tenant isolation rather than separate collections

## AI-agent gotchas
- Agents must handle the "collection already exists" case gracefully — `recreate_collection` drops data; use `get_or_create` pattern
- Batch upsert size matters: Qdrant recommends 100–500 vectors per batch; larger batches can cause gRPC timeouts
- Agents embedding documents concurrently and upserting in parallel must handle rate limits from embedding APIs separately from DB limits
- HNSW index quality degrades after heavy deletes — agent pipelines that frequently delete-and-re-insert should schedule periodic index optimization
- Never store raw PII in vector payload; agents must strip sensitive fields before upsert, not after
- Qdrant's filter-during-search (payload filters) is fast but only if the filter field is indexed — agent must call `create_payload_index` for filtered fields

## References
- https://qdrant.tech/documentation/
- https://weaviate.io/developers/weaviate
- https://milvus.io/docs
- https://docs.pinecone.io/
- https://github.com/pgvector/pgvector
- https://lakefs.io/blog/best-vector-databases/
