# Agent Integration — Vector Database Comparison

## When to use
- Starting a new RAG or semantic search project and selecting the vector DB technology.
- Migrating from a prototype DB (Chroma) to a production-grade one (Qdrant, Pinecone).
- Evaluating whether to add a separate vector DB or extend an existing PostgreSQL setup with pgvector.
- Designing a multi-agent system where different agents use different retrieval backends.

## When NOT to use
- Database is already selected and deployed; comparison analysis adds no value at this stage.
- Corpus is < 10K vectors and latency is not critical — any DB works; pick the simplest.
- Evaluating operational cost in isolation from query patterns; benchmarks without real queries are misleading.

## Where it fails / limitations
- Public benchmarks (ANN Benchmarks, VectorView) use synthetic datasets; your domain query distribution may differ significantly.
- Managed SaaS costs (Pinecone, Weaviate Cloud) scale non-linearly with vector count and query volume — model the cost before committing.
- pgvector IVFFlat recall degrades without periodic `VACUUM ANALYZE` — often omitted in naive benchmarks.
- HNSW index rebuild time is O(n log n) — for 100M+ vectors, re-indexing takes hours; plan for blue/green index strategy.
- Chroma's in-memory mode has no persistence; data loss on process restart is a common agent-side bug.
- Milvus requires dedicated infrastructure (etcd, MinIO, Pulsar) — operational burden is high for small teams.

## Agentic workflow
A database-selector subagent is invoked once at project initialization. It receives the corpus size, query latency requirement, team infrastructure, and hosting preference, then returns a ranked recommendation with rationale. For production systems, a benchmark subagent runs a representative sample of real queries against 2–3 candidate DBs and reports P50/P99 latency and recall@10 before the final decision is committed.

### Recommended subagents
- `db-selector` — Analyzes requirements (scale, hosting, filtering, latency) and outputs DB recommendation with rationale.
- `benchmark-runner` — Loads sample data into candidate DBs, runs query benchmark, returns recall and latency comparison table.
- `migration-planner` — Given current DB and target DB, generates a migration plan including re-embedding schedule and downtime estimate.

### Prompt pattern
```python
# DB selector prompt (structured output via tool)
DB_SELECTOR_PROMPT = """
Given these requirements, select the optimal vector database:
- Corpus size: {corpus_size} vectors
- Query latency SLA: {latency_sla}ms P95
- Hosting: {hosting_preference} (self-hosted / managed)
- Existing stack: {existing_stack}
- Primary use case: {use_case}
- Filtering needed: {filtering_complexity}

Return JSON: {"db": str, "rationale": str, "caveats": list[str]}
"""
```

Quick selection logic (embed in db-selector):
```python
def select_db(corpus_size: int, managed: bool, has_postgres: bool,
              needs_graph: bool, scale_1b: bool) -> str:
    if corpus_size < 50_000 and not managed:
        return "chroma"  # Prototype
    if has_postgres and corpus_size < 5_000_000:
        return "pgvector"  # No new infra
    if needs_graph:
        return "weaviate"
    if scale_1b or managed:
        return "pinecone"
    return "qdrant"  # Default production self-hosted
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `qdrant-client` | Qdrant Python client | `pip install qdrant-client` / qdrant.tech/documentation |
| `weaviate-client` | Weaviate v4 Python client | `pip install weaviate-client` / weaviate.io/developers |
| `chromadb` | Chroma Python client | `pip install chromadb` / docs.trychroma.com |
| `pinecone` | Pinecone Python client | `pip install pinecone` / docs.pinecone.io |
| `pgvector` | PostgreSQL vector extension + Python adapter | `pip install pgvector psycopg2` / github.com/pgvector/pgvector |
| `pymilvus` | Milvus Python client | `pip install pymilvus` / milvus.io/docs |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Qdrant Cloud | SaaS | Yes | Free 1GB cluster; REST + gRPC; strong filtering |
| Qdrant OSS | OSS | Yes | Docker single-node; Kubernetes cluster mode |
| Weaviate Cloud | SaaS | Yes | 14-day free sandbox; GraphQL native |
| Weaviate OSS | OSS | Yes | Knowledge graph + hybrid search |
| Pinecone | SaaS | Yes | Serverless tier; best for 1B+; no self-hosted |
| Chroma | OSS | Yes | Dev only; no production SLA |
| pgvector | OSS | Yes | PostgreSQL extension; excellent for existing PG stacks |
| Milvus | OSS / Cloud | Yes | GPU support; enterprise scale; complex ops |

## Templates & scripts
See `templates.md` for Qdrant, pgvector, Pinecone, and Chroma quickstart templates.

Selection scorecard helper:
```python
from dataclasses import dataclass

@dataclass
class DBRequirements:
    corpus_vectors: int
    latency_ms_p95: int
    managed: bool
    has_postgres: bool
    needs_graph: bool
    needs_hybrid_native: bool
    team_size: int  # ops headcount

RECOMMENDATIONS = {
    "chroma":    {"max_vectors": 500_000, "managed": False, "graph": False},
    "pgvector":  {"max_vectors": 5_000_000, "managed": False, "graph": False},
    "qdrant":    {"max_vectors": 500_000_000, "managed": True, "graph": False},
    "weaviate":  {"max_vectors": 100_000_000, "managed": True, "graph": True},
    "pinecone":  {"max_vectors": 10_000_000_000, "managed": True, "graph": False},
    "milvus":    {"max_vectors": 10_000_000_000, "managed": False, "graph": False},
}

def recommend(req: DBRequirements) -> str:
    if req.has_postgres and req.corpus_vectors < 5_000_000:
        return "pgvector"
    if req.needs_graph:
        return "weaviate"
    if req.corpus_vectors > 500_000_000 or req.managed:
        return "pinecone"
    if req.corpus_vectors < 50_000:
        return "chroma"
    return "qdrant"
```

## Best practices
- Default to Qdrant for new self-hosted production RAG systems; it has the best balance of performance, filtering, and operational simplicity.
- Use pgvector when the team already operates PostgreSQL and corpus is under 5M vectors — zero new infra, ACID transactions, SQL filtering.
- Never use Chroma as the only vector store in production; it lacks replication, auth, and backup primitives.
- Run a 3-day production load test before committing to a managed SaaS DB — cost curves are non-obvious under real query patterns.
- Index type choice: HNSW for high-recall retrieval; IVFFlat for faster build time when recall@10 > 0.95 is not required.
- Apply scalar quantization (int8) for corpora > 10M vectors to reduce memory by 4x with < 1% recall loss.
- Always store the raw vector alongside metadata in a backup store (PostgreSQL or S3) — vector DBs are not the source of truth.

## AI-agent gotchas
- Agents that read DB benchmark articles choose the winner of the latest public benchmark — which may not reflect your corpus distribution. Always run your own benchmark with your actual query distribution.
- Chroma's default persistence mode uses DuckDB+Parquet; concurrent write access from multiple agent processes causes corruption — use client-server mode.
- pgvector requires `SET ivfflat.probes = N` per connection to improve recall — agents using connection pools may not set this, silently getting recall@10 of 0.6 instead of 0.95.
- Pinecone serverless pricing charges per read unit (RU); a single `query(top_k=100)` costs 10x more than `top_k=10` — agents that default to large top_k blow the cost budget.
- Dimension mismatch: embedding model changes produce vectors of different dimension; inserting into an existing collection fails silently in some clients — validate dimension at insert time.
- Human-in-loop checkpoint: DB migration (changing vector DB technology) requires re-embedding the full corpus — validate that the new embedding model produces semantically equivalent results on a sample before cutting over.

## References
- https://benchmark.vectorview.ai/vectordbs.html — Vector DB benchmark comparison
- https://github.com/pgvector/pgvector — pgvector GitHub
- https://qdrant.tech/documentation/ — Qdrant documentation
- https://docs.pinecone.io/ — Pinecone documentation
- https://weaviate.io/developers/weaviate — Weaviate documentation
- https://ann-benchmarks.com/ — ANN Benchmarks (recall vs. throughput)
