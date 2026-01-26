# GraphRAG: Knowledge Graph-Enhanced Retrieval

> Graph-based Retrieval-Augmented Generation for complex multi-hop queries.

## Overview

GraphRAG combines knowledge graphs with vector retrieval to answer questions requiring entity relationships and global reasoning. Unlike standard RAG (semantic similarity over chunks), GraphRAG builds structured entity-relationship graphs and uses community detection for hierarchical summarization.

## When to Use GraphRAG

| Scenario | Standard RAG | GraphRAG |
|----------|--------------|----------|
| Simple factual queries | Preferred | Overkill |
| Multi-hop reasoning | Struggles | Excels |
| "What are main themes?" | Cannot answer | Designed for |
| Entity relationships | Limited | Core strength |
| Global sensemaking | Poor | Excellent |

**Use GraphRAG when:**
- Questions require understanding relationships between entities
- Need to answer "global" questions about entire corpus
- Multi-hop reasoning is required (A relates to B, B relates to C)
- Want hierarchical summaries at different granularities

**Stick with Standard RAG when:**
- Simple fact lookup
- Single-document queries
- Low latency requirements
- Limited compute budget

## Architecture

```
Documents
    |
    v
[Chunking] --> [Entity Extraction] --> [Relationship Extraction]
                      |                          |
                      v                          v
              [Entity Resolution]        [Graph Construction]
                      |                          |
                      +----------+---------------+
                                 |
                                 v
                    [Knowledge Graph (Neo4j/NetworkX)]
                                 |
                                 v
                    [Community Detection (Leiden)]
                                 |
                                 v
                    [Hierarchical Summarization]
                                 |
                                 v
                    [Indexed Graph + Summaries]

Query
    |
    v
[Query Analysis] --> [Entity Recognition]
                              |
                              v
                    [Retrieval Strategy Selection]
                              |
        +---------------------+---------------------+
        |                     |                     |
        v                     v                     v
  [Local Search]      [Global Search]      [Hybrid Search]
        |                     |                     |
        v                     v                     v
  [Subgraph]         [Community Summaries]  [Vector + Graph]
        |                     |                     |
        +---------------------+---------------------+
                              |
                              v
                    [Context Assembly]
                              |
                              v
                    [LLM Synthesis]
                              |
                              v
                    [Response]
```

## Core Components

### 1. Knowledge Graph Construction

**Entity Extraction:**
- LLM-based extraction (GPT-4, Claude)
- Traditional NER (SpaCy, GliNER)
- Hybrid approaches (NER + LLM refinement)

**Relationship Extraction:**
- LLM prompting with schema guidance
- Co-occurrence analysis
- Dependency parsing

**Entity Resolution:**
- Embedding-based similarity
- LLM-assisted disambiguation
- Rule-based merging

### 2. Community Detection

Microsoft GraphRAG uses the **Leiden algorithm** hierarchically:

| Level | Description |
|-------|-------------|
| 0 | Original graph, fine-grained communities |
| 1 | Aggregated communities, broader themes |
| 2+ | Higher-level abstractions |
| Root | Entire corpus summary |

**Parameters:**
- `max_cluster_size`: Default 10
- `resolution`: Controls granularity
- `iterations`: Refinement passes

### 3. Retrieval Strategies

| Strategy | Description | Best For |
|----------|-------------|----------|
| **Local Search** | Subgraph traversal from query entities | Specific entity questions |
| **Global Search** | Community summaries map-reduce | Theme/overview questions |
| **Hybrid Search** | Vector + graph + keyword | General queries |

### 4. Graph Traversal

**Traversal patterns:**
- **1-hop**: Direct relationships
- **2-hop**: Intermediate connections
- **N-hop**: Configurable depth
- **Weighted**: Relationship strength scoring

## Technology Stack

### Graph Databases

| Database | Best For | Integration |
|----------|----------|-------------|
| **Neo4j** | Production, Cypher queries | neo4j-graphrag-python |
| **NetworkX** | Prototyping, in-memory | Microsoft GraphRAG |
| **Memgraph** | Real-time, high throughput | Cypher compatible |
| **Amazon Neptune** | AWS native, managed | Gremlin/SPARQL |

### Vector Databases (Hybrid)

| Database | Graph Support |
|----------|---------------|
| **Weaviate** | Built-in knowledge graph |
| **Qdrant** | External graph integration |
| **Chroma** | External graph integration |
| **pgvector** | PostgreSQL graph extensions |

### Frameworks

| Framework | Focus |
|-----------|-------|
| **Microsoft GraphRAG** | Full pipeline, community detection |
| **LlamaIndex PropertyGraph** | Flexible graph construction |
| **LangChain** | Graph retrievers, Neo4j integration |
| **Neo4j GraphRAG Python** | Production-ready, hybrid search |
| **LightRAG** | 10x token reduction, efficient |

## Performance Benchmarks

| Metric | Standard RAG | GraphRAG | Improvement |
|--------|--------------|----------|-------------|
| Comprehensiveness | Baseline | +30-50% | Significant |
| Multi-hop accuracy | 45% | 73% | +62% |
| Hallucination rate | Higher | Lower | -40% |
| Indexing cost | Low | High | 5-10x more tokens |
| Query latency | Fast | Medium | 2-3x slower |

## Cost Considerations

| Operation | Token Usage | Optimization |
|-----------|-------------|--------------|
| Entity extraction | ~500 tokens/chunk | Batch processing |
| Relationship extraction | ~300 tokens/chunk | Schema constraints |
| Community summarization | ~1000 tokens/community | Caching |
| Query (global) | ~2000 tokens | Summary caching |
| Query (local) | ~500 tokens | Subgraph pruning |

**Cost reduction strategies:**
- LightRAG: 10x token reduction
- Traditional NER + LLM refinement
- Incremental indexing
- Community summary caching

## References

- [Microsoft GraphRAG](https://github.com/microsoft/graphrag)
- [GraphRAG Paper (arXiv:2404.16130)](https://arxiv.org/abs/2404.16130)
- [Neo4j GraphRAG Python](https://github.com/neo4j/neo4j-graphrag-python)
- [LlamaIndex Property Graphs](https://docs.llamaindex.ai/en/stable/examples/property_graph/)
- [Weaviate GraphRAG](https://weaviate.io/blog/graph-rag)

## Related Files

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Implementation checklist |
| [examples.md](examples.md) | Code examples |
| [templates.md](templates.md) | Configuration templates |
| [llm-prompts.md](llm-prompts.md) | Entity/relationship extraction prompts |
