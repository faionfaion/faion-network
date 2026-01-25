# RAG Engineer Skill

> **Entry Point:** Invoked via [/faion-ml-engineer](../faion-ml-engineer/CLAUDE.md)

## When to Use

- Building RAG (Retrieval Augmented Generation) systems
- Document chunking and embedding generation
- Vector database setup (Qdrant, Weaviate, Chroma)
- Hybrid search and reranking
- RAG evaluation and optimization
- Agentic RAG patterns

## Overview

Specializes in RAG pipeline design and implementation.

**Methodologies:** 22 | **Focus:** Retrieval, embeddings, vector search

## Quick Reference

| Component | Files |
|-----------|-------|
| Chunking | chunking-basics.md, chunking-advanced.md |
| Embeddings | embedding-basics.md, embedding-generation.md, embedding-models.md |
| Vector DBs | db-qdrant.md (recommended), db-weaviate.md, db-chroma.md |
| Retrieval | hybrid-search-basics.md, reranking-basics.md |
| RAG | rag-architecture.md, rag-implementation.md, rag-eval-metrics.md |

## Methodology Count

- Chunking: 2 methodologies
- Embeddings: 4 methodologies
- Vector DBs: 5 methodologies
- Retrieval: 4 methodologies
- RAG Systems: 7 methodologies

**Total: 22**

## Recommended Stack

- **Vector DB:** Qdrant (production) or Chroma (dev)
- **Embeddings:** text-embedding-3-large (OpenAI) or voyage-3
- **Reranking:** Cohere rerank-3 or MixedBread
- **Framework:** LangChain or LlamaIndex

## Related

- Parent: [faion-ml-engineer](../faion-ml-engineer/CLAUDE.md)
- Uses: faion-llm-integration (embeddings API)
- Peers: faion-ai-agents (agentic RAG)

---

*RAG Engineer v1.0*
