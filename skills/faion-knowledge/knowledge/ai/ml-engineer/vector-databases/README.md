# Vector Databases

Comprehensive guide for storing, indexing, and querying vector embeddings in RAG pipelines and semantic search applications.

## Overview

Vector databases are specialized storage systems optimized for high-dimensional vector operations. They enable semantic search by finding similar items based on embedding distance rather than exact keyword matching.

**Core capabilities:**
- Store and index high-dimensional vectors (embeddings)
- Perform fast approximate nearest neighbor (ANN) search
- Filter results by metadata alongside vector similarity
- Scale to millions or billions of vectors

---

## Database Comparison

| Database | Type | Best For | Scale | Hosting | Hybrid Search |
|----------|------|----------|-------|---------|---------------|
| **Qdrant** | Purpose-built | Production RAG, complex filtering | 100M+ | Self/Cloud | Native |
| **Weaviate** | Graph + Vector | Knowledge graphs, semantic search | 50M+ | Self/Cloud | Native |
| **Milvus** | Purpose-built | Enterprise scale, high throughput | 1B+ | Self/Cloud | Native |
| **Pinecone** | Managed | Serverless, zero-ops | 1B+ | Cloud only | Native |
| **pgvector** | Extension | Existing PostgreSQL apps | 10-100M | Self-hosted | Via SQL |
| **Chroma** | Embedded | Prototyping, local dev | 1M | In-process | Basic |

### Performance Benchmarks (2025)

| Database | Latency (p95) | Throughput | Recall@10 | Memory Efficiency |
|----------|---------------|------------|-----------|-------------------|
| Milvus | 2-5ms | 100K+ QPS | 95%+ | Good (tiered storage) |
| Qdrant | 5-15ms | 40-50 QPS @ 50M | 99% | Excellent (quantization) |
| Weaviate | 10-50ms | High | 95%+ | Moderate |
| Pinecone | 2-10ms | High | 98%+ | Managed |
| pgvector | 20-100ms | Moderate | 90-95% | PostgreSQL RAM |

*Benchmarks vary by hardware, index type, and dataset. Test with your own data.*

### Popularity & Adoption (2025)

| Database | GitHub Stars | Monthly Docker Pulls | Community |
|----------|--------------|----------------------|-----------|
| Milvus | ~35,000 | ~700K | CNCF project |
| Qdrant | ~20,000 | ~500K | Active OSS |
| Weaviate | ~12,000 | ~1M+ | Strong enterprise |
| Chroma | ~15,000 | - | Growing fast |
| pgvector | ~12,000 | - | PostgreSQL ecosystem |

---

## Selection Guide

### Decision Tree

```
START: What's your primary constraint?

├── Need managed service, zero ops?
│   └── Pinecone (serverless, predictable pricing)
│
├── Have existing PostgreSQL infrastructure?
│   └── pgvector (SQL integration, familiar tooling)
│
├── Rapid prototyping / local development?
│   └── Chroma (simple API, in-memory)
│
├── Production self-hosted?
│   ├── Need complex filtering + moderate scale?
│   │   └── Qdrant (Rust perf, excellent filters)
│   │
│   ├── Need knowledge graph features?
│   │   └── Weaviate (GraphQL, cross-references)
│   │
│   └── Need extreme scale (1B+ vectors)?
│       └── Milvus (distributed, GPU support)
│
└── Enterprise with compliance requirements?
    └── Milvus/Zilliz or Weaviate Cloud (SOC2, HIPAA)
```

### Use Case Recommendations

| Use Case | Recommended | Why |
|----------|-------------|-----|
| **RAG chatbot** | Qdrant, Weaviate | Hybrid search, metadata filtering |
| **Semantic search** | Pinecone, Qdrant | Low latency, high recall |
| **E-commerce similarity** | Milvus, Pinecone | Scale, real-time updates |
| **Document retrieval** | Weaviate | Knowledge graph, relationships |
| **Existing Django/Rails app** | pgvector | SQL integration, no new infra |
| **MVP / hackathon** | Chroma | Zero setup, fast iteration |
| **Multi-tenant SaaS** | Qdrant, Pinecone | Namespace isolation |
| **Image/video similarity** | Milvus | GPU acceleration, large vectors |

### Cost Considerations

| Database | Free Tier | Starting Price | Notes |
|----------|-----------|----------------|-------|
| Pinecone | Yes (limited) | ~$70/month | Serverless billing |
| Qdrant Cloud | 1GB free forever | ~$27-102/month | Storage-based |
| Weaviate Cloud | 14-day trial | ~$25/month | Cluster-based |
| Milvus (Zilliz) | Free tier | Contact sales | Enterprise pricing |
| pgvector | N/A | Your PostgreSQL cost | Extension is free |
| Chroma | N/A | Free (self-hosted) | No cloud offering |

---

## Database Deep Dives

### Qdrant (Recommended for Production RAG)

**Strengths:**
- Written in Rust for performance and safety
- Excellent payload filtering with indexed fields
- Native hybrid search (dense + sparse vectors)
- Binary quantization for 32x memory reduction
- Strong multi-tenancy support

**Weaknesses:**
- Smaller community than Milvus
- Less GPU acceleration
- Self-hosting requires ops knowledge

**Best for:** Production RAG systems, applications requiring complex metadata filtering, multi-tenant SaaS.

### Weaviate

**Strengths:**
- Native GraphQL API
- Knowledge graph with cross-references
- Built-in vectorizers (text2vec modules)
- Hybrid search (BM25 + vector)
- Strong semantic understanding

**Weaknesses:**
- Higher memory usage at scale (100M+ vectors)
- Slower than pure vector DBs for simple queries
- Graph features add complexity

**Best for:** Knowledge management, document relationships, semantic search with context.

### Milvus

**Strengths:**
- Highest throughput (100K+ QPS)
- Most indexing strategies (IVF, HNSW, DiskANN, GPU)
- Distributed architecture for massive scale
- CNCF project with strong governance
- Tiered storage (hot/warm/cold)

**Weaknesses:**
- Complex to deploy and operate
- Higher dimensional embeddings impact performance
- Steeper learning curve

**Best for:** Enterprise scale, billion-vector datasets, high-throughput requirements.

### Pinecone

**Strengths:**
- True serverless (pay per query)
- Zero operational burden
- Consistent low latency
- Excellent documentation
- Simple SDK

**Weaknesses:**
- Cloud-only (no self-hosting)
- Vendor lock-in
- Can be expensive at scale
- Less filtering flexibility

**Best for:** Teams without DevOps resources, startups, rapid development.

### pgvector

**Strengths:**
- Uses existing PostgreSQL infrastructure
- Full SQL capabilities (JOINs, transactions)
- Familiar tooling and ecosystem
- ACID compliance
- Django/Rails ORM support

**Weaknesses:**
- Limited to ~100M vectors before performance degrades
- Fewer ANN algorithms than specialized DBs
- No native hybrid search

**Best for:** Applications already using PostgreSQL, moderate scale requirements.

### Chroma

**Strengths:**
- Simplest API
- In-process (no network calls)
- Persistent storage option
- LangChain/LlamaIndex integration
- Great for learning and prototyping

**Weaknesses:**
- Not designed for production scale
- Limited filtering capabilities
- Single-node only

**Best for:** Prototyping, local development, learning vector databases.

---

## Indexing Strategies

### HNSW (Hierarchical Navigable Small World)

**Best for:** Most use cases, balanced speed/accuracy

| Parameter | Default | Recommended | Effect |
|-----------|---------|-------------|--------|
| M | 16 | 12-48 | Connections per node. Higher = better recall, more memory |
| ef_construction | 100 | 100-500 | Build quality. Higher = better index, slower build |
| ef_search | 40 | 50-200 | Search quality. Higher = better recall, slower search |

### IVF (Inverted File Index)

**Best for:** Large datasets, faster build time

| Parameter | Default | Recommended | Effect |
|-----------|---------|-------------|--------|
| nlist | sqrt(n) | sqrt(n) to 4*sqrt(n) | Number of clusters |
| nprobe | 1 | nlist/10 to nlist/4 | Clusters to search |

### Quantization

| Method | Memory Reduction | Speed Impact | Accuracy Loss |
|--------|------------------|--------------|---------------|
| None | 1x | Baseline | None |
| Scalar (int8) | 4x | Faster | 1-2% |
| Product (PQ) | 8-32x | Faster | 3-5% |
| Binary | 32x | Fastest | 5-10% |

**Recommendation:** Start with scalar quantization + rescoring for production. Binary quantization for cost-sensitive workloads.

---

## Hybrid Search

Combine dense vector similarity with sparse keyword search for best results.

**Why hybrid search matters:**
- Vector search excels at semantic similarity, handles typos
- Keyword search excels at exact matches, names, acronyms
- Hybrid captures both strengths

**Implementation approaches:**

1. **Native hybrid** (Weaviate, Qdrant): Single API call combines both
2. **Reciprocal Rank Fusion (RRF)**: Merge results from separate searches
3. **Late interaction**: Use cross-encoder to rerank combined results

**Alpha parameter (Weaviate):**
- `alpha=0`: Pure BM25 keyword search
- `alpha=0.5`: Balanced hybrid
- `alpha=1`: Pure vector search

**Recommendation:** Start with `alpha=0.7` (favor vectors), tune based on evaluation.

---

## LLM Usage Tips

### For Qdrant

```
When using Qdrant in RAG pipelines:
1. Always create payload indexes for filterable fields
2. Use batch upserts (100-500 points per batch)
3. Enable quantization for production (scalar or binary)
4. Prefer gRPC over HTTP for high throughput
5. Use score_threshold to filter low-quality matches
```

### For Weaviate

```
When using Weaviate in RAG pipelines:
1. Define schema with property types for better filtering
2. Use hybrid search with alpha=0.7 as starting point
3. Create cross-references for document relationships
4. Leverage GraphQL for complex queries
5. Consider text2vec modules for automatic embedding
```

### For pgvector

```
When using pgvector in RAG pipelines:
1. Always create HNSW index (not IVFFlat) for production
2. Use parameterized queries to leverage plan caching
3. Set hnsw.ef_search based on recall needs
4. Create partial indexes for filtered queries
5. VACUUM ANALYZE after bulk inserts
```

---

## External Links

### Official Documentation

| Database | Documentation | GitHub |
|----------|---------------|--------|
| Qdrant | [qdrant.tech/documentation](https://qdrant.tech/documentation/) | [qdrant/qdrant](https://github.com/qdrant/qdrant) |
| Weaviate | [weaviate.io/developers](https://weaviate.io/developers/weaviate) | [weaviate/weaviate](https://github.com/weaviate/weaviate) |
| Milvus | [milvus.io/docs](https://milvus.io/docs) | [milvus-io/milvus](https://github.com/milvus-io/milvus) |
| Pinecone | [docs.pinecone.io](https://docs.pinecone.io/) | N/A (closed source) |
| pgvector | [github.com/pgvector](https://github.com/pgvector/pgvector) | [pgvector/pgvector](https://github.com/pgvector/pgvector) |
| Chroma | [docs.trychroma.com](https://docs.trychroma.com/) | [chroma-core/chroma](https://github.com/chroma-core/chroma) |

### Benchmarks & Comparisons

- [Qdrant Benchmarks](https://qdrant.tech/benchmarks/)
- [ANN Benchmarks](https://ann-benchmarks.com/)
- [Vector Database Comparison (LiquidMetal)](https://liquidmetal.ai/casesAndBlogs/vector-comparison/)
- [ZenML Vector DB Comparison](https://www.zenml.io/blog/vector-databases-for-rag)

### Learning Resources

- [Pinecone Learning Center](https://www.pinecone.io/learn/)
- [Weaviate Blog](https://weaviate.io/blog)
- [Qdrant Blog](https://qdrant.tech/articles/)

---

## File Structure

```
vector-databases/
├── README.md           # This file - overview and comparison
├── checklist.md        # Checklists for selection, setup, production
├── examples.md         # Code examples for each database
├── templates.md        # Configuration and deployment templates
└── llm-prompts.md      # Prompts for LLM assistance
```

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [faion-rag-engineer](../faion-rag-engineer/CLAUDE.md) | RAG pipeline integration |
| [faion-llm-integration](../faion-llm-integration/CLAUDE.md) | Embedding generation |
| [faion-infrastructure-engineer](../../faion-infrastructure-engineer/CLAUDE.md) | Deployment and scaling |

---

*Vector Databases v2.0*
*Part of faion-ml-engineer skill*

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Vector DB selection | sonnet | Tool evaluation |
| Index optimization | sonnet | Performance tuning |
| Query optimization | sonnet | Search tuning |
