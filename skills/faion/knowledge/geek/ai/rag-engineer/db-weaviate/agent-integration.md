# Agent Integration — Weaviate Vector Database

## When to use
- Knowledge graph capabilities are needed: entities with cross-references (Author → Document → Topic).
- Native hybrid search (vector + BM25) is required without client-side fusion code.
- GraphQL-based querying fits the team's existing tooling or API gateway.
- Corpus contains multi-modal data (text + images) — Weaviate supports multi-vector objects.
- Self-hosted deployment on Kubernetes at 10M–100M vector scale.

## When NOT to use
- Simple RAG prototype with no graph relationships — Chroma or Qdrant are simpler to set up.
- Team is unfamiliar with GraphQL; prefer Qdrant (REST/gRPC) for API simplicity.
- Payload filtering at high cardinality is the primary concern — Qdrant's payload filter performance exceeds Weaviate's at scale.
- Cost-sensitive managed deployment at 1B+ vectors — Pinecone or Milvus have lower per-vector managed pricing.

## Where it fails / limitations
- GraphQL schema changes require collection recreation — no in-place schema migration support.
- Weaviate v4 Python client (`weaviate-client >= 4.0`) is incompatible with v3 client code; migration is breaking.
- `AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true` is insecure for production — always configure API key or OIDC auth.
- BM25 index rebuild on large collections is slow and blocks reads during the process.
- Cross-reference traversal in GraphQL adds round-trips; deeply nested graphs degrade query latency.
- Weaviate Cloud (WCS) free tier has 14-day sandbox expiry — do not use for persistent agent memory.

## Agentic workflow
An indexer subagent ingests documents and creates cross-reference links (Document → Author, Document → Topic) at write time. The retriever subagent executes hybrid queries against the collection, using `alpha=0.5` by default and adjusting dynamically based on query classification. A graph-traversal subagent follows cross-references to enrich retrieved chunks with author metadata or related topic chunks. Results flow to the generator subagent for grounded answer synthesis.

### Recommended subagents
- `weaviate-indexer` — Batch-inserts documents with vectors and cross-references; handles schema creation.
- `weaviate-retriever` — Executes hybrid queries with dynamic alpha; returns scored objects with metadata.
- `graph-enricher` — Traverses cross-references to pull related entities (authors, topics) for retrieved chunks.

### Prompt pattern
```python
import weaviate
from weaviate.classes.query import MetadataQuery

client = weaviate.connect_to_local()
docs = client.collections.get("Document")

# Hybrid search call
response = docs.query.hybrid(
    query=user_query,
    vector=query_embedding,
    alpha=0.6,          # 60% semantic, 40% keyword
    limit=10,
    return_metadata=MetadataQuery(score=True, explain_score=True)
)

for obj in response.objects:
    print(f"Score: {obj.metadata.score:.3f}")
    print(f"Text: {obj.properties['text'][:200]}")
```

GraphQL cross-reference traversal:
```python
result = client.graphql_raw_query("""
{
  Get {
    Document(
      nearVector: {vector: [...], certainty: 0.75}
      limit: 5
    ) {
      text source
      hasAuthor { ... on Author { name email } }
      _additional { certainty }
    }
  }
}
""")
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `weaviate-client` (v4) | Official Python client; async support, batch API | `pip install weaviate-client` / weaviate.io/developers/weaviate/client-libraries/python |
| `docker` | Run Weaviate locally via official Docker image | `docker run semitechnologies/weaviate:latest` |
| `helm` | Deploy Weaviate on Kubernetes | helm.weaviate.io |
| `weaviate-cli` | Admin CLI for schema and data management | `pip install weaviate-cli` / github.com/weaviate/weaviate-cli |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Weaviate Cloud (WCS) | SaaS | Yes | Managed; free sandbox (14-day); production paid |
| Weaviate OSS (Docker) | OSS | Yes | Self-hosted; full feature parity with WCS |
| Weaviate + OpenAI module | SaaS/OSS | Yes | `text2vec-openai` auto-embeds at index time |
| Weaviate + Cohere module | SaaS/OSS | Yes | `reranker-cohere` module for built-in reranking |
| LlamaIndex + Weaviate | OSS | Yes | `WeaviateVectorStore` integration |

## Templates & scripts
See `templates.md` for schema creation, batch insert, hybrid search, and cross-reference templates.

Batch insert with vectors (under 35 lines):
```python
import weaviate
from weaviate.classes.config import Configure, Property, DataType

client = weaviate.connect_to_local()

# Create collection (idempotent check)
if not client.collections.exists("Document"):
    client.collections.create(
        name="Document",
        vectorizer_config=Configure.Vectorizer.none(),
        properties=[
            Property(name="text", data_type=DataType.TEXT),
            Property(name="source", data_type=DataType.TEXT),
            Property(name="page", data_type=DataType.INT),
        ],
    )

docs = client.collections.get("Document")

# Batch insert
with docs.batch.dynamic() as batch:
    for doc in document_list:
        batch.add_object(
            properties={"text": doc["text"], "source": doc["source"], "page": doc["page"]},
            vector=doc["embedding"],
        )

client.close()
```

## Best practices
- Always call `client.close()` or use `with weaviate.connect_to_local() as client:` — unclosed connections leak gRPC resources.
- Set `vectorizer_config=Configure.Vectorizer.none()` and manage embeddings externally — vendor-specific vectorizer modules add coupling and latency you do not control.
- Use `batch.dynamic()` for inserts; it auto-adjusts batch size based on server response time to maximize throughput.
- Add `skip_vectorization=True` on metadata properties (category, date, IDs) to avoid embedding non-semantic fields.
- Configure HNSW parameters at collection creation — `ef=100, max_connections=16` is a safe production default; increase `ef` for higher recall requirements.
- Use `Filter.by_property()` for pre-filter before vector search; Weaviate applies filters before ANN search (not post-filter like some DBs).
- Monitor Weaviate's `/v1/meta` endpoint for shard health and index status in agent health checks.

## AI-agent gotchas
- v3 and v4 Python client APIs are incompatible; agents using older LangChain/LlamaIndex integrations may use v3 under the hood — check which client version is installed.
- Weaviate's `certainty` metric is model-dependent; comparing certainty scores across collections using different vectorizers is meaningless.
- Cross-reference inserts require the referenced object to exist first — batch ordering matters; insert target objects before source objects.
- Hybrid search `alpha` is not the same as Qdrant's `alpha`; Weaviate's `alpha=0` means pure BM25, `alpha=1` means pure vector — opposite intuition risk.
- Human-in-loop checkpoint: schema changes (adding/removing properties) require collection drop and re-index in Weaviate v4 — always run schema migrations in a staging environment first.

## References
- https://weaviate.io/developers/weaviate — Weaviate documentation
- https://weaviate.io/developers/weaviate/client-libraries/python — Python client v4 guide
- https://weaviate.io/developers/wcs — Weaviate Cloud
- https://weaviate.io/blog/knowledge-graphs — Knowledge graphs with Weaviate
- https://weaviate.io/developers/weaviate/search/hybrid — Hybrid search reference
