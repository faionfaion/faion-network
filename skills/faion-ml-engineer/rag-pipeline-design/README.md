# RAG Pipeline Design

Production-ready RAG pipeline architecture covering components, orchestration, caching, monitoring, and deployment patterns.

## Overview

RAG (Retrieval-Augmented Generation) grounds LLM responses in domain-specific data through a pipeline of retrieval and generation components. Modern RAG systems have evolved from naive single-stage retrieval to advanced modular and agentic architectures.

## Architecture Tiers

| Tier | Description | When to Use |
|------|-------------|-------------|
| **Naive RAG** | Simple retrieve-then-generate | Straightforward, repetitive queries ("What is the vacation policy?") |
| **Advanced RAG** | Query rewriting, reranking, hybrid search | Ambiguous or indirect user queries |
| **Modular RAG** | Pluggable components, parallel retrieval | Custom requirements, multiple data sources |
| **Agentic RAG** | Autonomous agents with tools | Complex reasoning, workflow execution, multi-step tasks |

## Core Pipeline Components

```
User Query
    |
    v
[Query Processing] --> Query rewriting, expansion, HyDE
    |
    v
[Retrieval Layer] --> Vector search + keyword search + metadata filtering
    |
    v
[Post-Retrieval] --> Reranking, deduplication, compression
    |
    v
[Context Assembly] --> Prompt construction, citation formatting
    |
    v
[Generation] --> LLM inference with retrieved context
    |
    v
[Post-Processing] --> Fact-checking, citation validation, guardrails
    |
    v
Response
```

## Component Stack

| Component | Options | Selection Criteria |
|-----------|---------|-------------------|
| **Embedding Model** | OpenAI text-embedding-3, Voyage-3-large, Cohere embed-v3, BGE | Quality vs cost; Voyage-3-large outperforms by 9-20% |
| **Vector Database** | Pinecone, Qdrant, Weaviate, Milvus, Chroma, pgvector | Managed vs self-hosted; scale requirements |
| **Chunking** | Fixed-size, semantic, recursive, hierarchical | Document type; single-topic vs multi-topic |
| **Orchestration** | LangChain, LlamaIndex, DSPy, Pathway | Prototyping speed vs production robustness |
| **Observability** | LangSmith, Langfuse, Prometheus + Grafana | Open-source vs managed; tracing depth |

## Vector Database Selection

| Database | Best For | Key Features |
|----------|----------|--------------|
| **Pinecone** | Managed, enterprise | Auto-scaling, multi-region, SOC 2, 40KB metadata/vector |
| **Qdrant** | Self-hosted production | Rust performance, hybrid search, rich filtering |
| **Weaviate** | Knowledge graphs | GraphQL API, hybrid search, modules ecosystem |
| **Milvus** | Large-scale deployments | GPU acceleration, distributed architecture |
| **Chroma** | Local development | Simple API, fast prototyping |
| **pgvector** | Existing PostgreSQL | No new infra, familiar tooling |

## Chunking Strategy Matrix

| Document Type | Recommended Strategy | Chunk Size |
|---------------|---------------------|------------|
| Short, single-purpose (FAQs, tickets) | No chunking / document-level | Full document |
| Code documentation | Header-based, recursive | 400-512 tokens |
| Long-form articles | Semantic chunking | 400-800 tokens |
| Technical manuals | Hierarchical | Parent: 1000, Child: 200 |
| Legal documents | Paragraph-based | 300-500 tokens |

**Performance benchmarks:**
- Page-level: 0.648 accuracy, lowest variance (NVIDIA benchmark)
- Semantic: +9% recall over fixed-size
- RecursiveCharacterTextSplitter (400-512 tokens): 85-90% recall, good default

## Retrieval Patterns

### Hybrid Search (Recommended)

Combine vector similarity with keyword matching:

```
Hybrid Score = alpha * vector_score + (1 - alpha) * bm25_score
```

| Pattern | Description |
|---------|-------------|
| **Vector + BM25** | Best general-purpose approach |
| **Vector + Metadata** | Filter by source, date, category |
| **Multi-query** | Generate query variations, merge results |
| **HyDE** | Embed hypothetical answer, not query |
| **Parent-child** | Retrieve small chunks, return parent context |

### Advanced Retrieval

| Technique | When to Use |
|-----------|-------------|
| **Reranking** | Improve top-K precision; Cohere, BGE rerankers |
| **GraphRAG** | Entity relationships matter |
| **Agentic retrieval** | Complex reasoning, iterative search |
| **Tree-based** | Hierarchical document structures |

## Production Architecture

```
                    +------------------+
                    |   Load Balancer  |
                    +--------+---------+
                             |
              +--------------+--------------+
              |              |              |
    +---------+---+  +-------+-----+  +-----+-------+
    | Query API   |  | Query API   |  | Query API   |
    | (Replicas)  |  | (Replicas)  |  | (Replicas)  |
    +------+------+  +------+------+  +------+------+
           |                |                |
           +----------------+----------------+
                            |
              +-------------+-------------+
              |             |             |
    +---------+--+  +-------+---+  +------+------+
    | Vector DB  |  |  Redis    |  | LLM API /   |
    | Cluster    |  | (Cache)   |  | Local Model |
    +------------+  +-----------+  +-------------+
```

## Key Files

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Pre-deployment verification |
| [examples.md](examples.md) | Implementation code |
| [templates.md](templates.md) | Production-ready templates |
| [llm-prompts.md](llm-prompts.md) | RAG system prompts |

## Quick Decisions

**Choosing architecture tier:**
- Simple Q&A over docs → Naive/Advanced RAG
- Multiple data sources → Modular RAG
- Complex multi-step reasoning → Agentic RAG

**Choosing vector DB:**
- Prototype → Chroma
- Production self-hosted → Qdrant
- Production managed → Pinecone
- Have PostgreSQL → pgvector

**Choosing embedding model:**
- Quality-critical → Voyage-3-large
- Cost-sensitive → text-embedding-3-small
- Privacy-required → Local (e.g., BGE, E5)

## Performance Targets

| Metric | Target | Optimization |
|--------|--------|--------------|
| Query latency (p50) | <500ms | Caching, async processing |
| Query latency (p99) | <2s | Index tuning, hardware |
| Retrieval recall@10 | >85% | Chunking, embedding model |
| Answer relevance | >90% | Reranking, prompt engineering |


## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Pipeline architecture | opus | System design |
| Component integration | sonnet | Integration planning |
| Workflow orchestration | sonnet | Process design |

## Sources

- [RAG Architecture Explained 2025](https://orq.ai/blog/rag-architecture)
- [Azure RAG Design Guide](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-solution-design-and-evaluation-guide)
- [RAG in Production](https://coralogix.com/ai-blog/rag-in-production-deployment-strategies-and-practical-considerations/)
- [Best Chunking Strategies 2025](https://www.firecrawl.dev/blog/best-chunking-strategies-rag-2025)
- [Vector Databases Guide 2025](https://dev.to/klement_gunndu_e16216829c/vector-databases-guide-rag-applications-2025-55oj)
- [RAG Review 2025](https://ragflow.io/blog/rag-review-2025-from-rag-to-context)
