# Embedding Generation

## Overview

Embeddings are dense vector representations of text that capture semantic meaning. They enable similarity search, clustering, classification, and form the foundation of RAG systems. This methodology covers embedding models, generation strategies, batch processing, caching, and optimization techniques.

## When to Use

- Semantic search implementations
- Document similarity matching
- RAG pipeline construction
- Text clustering and classification
- Recommendation systems
- Anomaly detection in text

## Key Concepts

### Embedding Models Comparison (2025-2026)

| Model | Dimensions | Context | Provider | Cost (per 1M tokens) | MTEB Score |
|-------|------------|---------|----------|---------------------|------------|
| embed-v4 | 1024 | 512 | Cohere | $0.10 | 65.2 |
| text-embedding-3-large | 3072 | 8191 | OpenAI | $0.13 | 64.6 |
| voyage-3-large | 1536 | 32K | Voyage | $0.12 | 63.8 |
| voyage-3.5-lite | 1024 | 32K | Voyage | $0.02 | 66.1 |
| text-embedding-3-small | 1536 | 8191 | OpenAI | $0.02 | 62.3 |
| BGE-M3 | 1024 | 8192 | Local/HF | Free | 63.0 |
| nomic-embed-text | 768 | 8192 | Local/Ollama | Free | 61.5 |
| mistral-embed | 1024 | 8192 | Mistral | $0.10 | 77.8* |
| all-MiniLM-L6-v2 | 384 | 256 | Local/HF | Free | 58.0 |

*Note: mistral-embed scored highest in specific retrieval benchmarks.

### Model Selection Guide

| Use Case | Recommended Model | Reason |
|----------|-------------------|--------|
| Document retrieval/RAG | Cohere embed-v4, OpenAI 3-large | Long context, high recall |
| Budget-sensitive production | voyage-3.5-lite, OpenAI 3-small | Low cost, solid accuracy |
| Privacy/offline | BGE-M3, nomic-embed-text | Self-hosted, no API costs |
| Multilingual | Cohere embed-v4 | 100+ languages |
| Conversational/chat | Mistral Embed, E5-Small | Low latency |
| Summarization | BGE-base, Mistral Embed | Good semantic clustering |

### Provider Characteristics

**OpenAI:**
- text-embedding-3-large: 3072 dimensions, native dimension reduction via API
- Supports shortening embeddings via `dimensions` parameter
- Up to 8191 tokens per call
- Best for: General purpose, English/multilingual

**Cohere:**
- embed-v4: Multilingual, multimodal (text + images)
- Task-specific input types: search_document, search_query, classification, clustering
- Enterprise-grade SLAs
- Best for: Multilingual, enterprise search

**Voyage AI:**
- Built by Stanford researchers, specializes in RAG
- Training includes "tricky negatives" to prevent false matches
- Best for: Domain-specific RAG, legal/medical/code retrieval

**Local Models:**
- BGE-M3: Best self-hosted quality
- nomic-embed-text: Good balance of quality/speed
- all-MiniLM-L6-v2: Fastest, smallest footprint

## Files

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Implementation checklist |
| [examples.md](examples.md) | Code examples (OpenAI, Cohere, local) |
| [templates.md](templates.md) | Production service templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for embedding tasks |

## Best Practices

### 1. Model Selection
- Prototype with low-cost model (OpenAI 3-small or voyage-3.5-lite)
- Measure Recall@100 and p95 latency on your data
- Re-benchmark quarterly as models improve rapidly

### 2. Batching
- Always batch when embedding multiple texts
- Use 100-1000 items per batch for APIs
- Sort by length to minimize padding waste
- Token-count-based batching for optimal throughput

### 3. Caching
- Implement two-layer cache: exact match + semantic
- Use content-based keys (hash of text + model)
- Target 60-80% cache hit rate
- Consider Redis for sub-millisecond latency

### 4. Normalization
- Pre-normalize embeddings for cosine similarity
- Store normalized embeddings in vector DBs
- Use dot product for faster search on normalized vectors

### 5. Dimension Reduction
- Use native dimension reduction when available (OpenAI 3-x models)
- Balance: 512-1024 dimensions for production
- Quantize to INT8 for 4-10x RAM reduction with <1% recall loss

### 6. Two-Stage Retrieval
- Cheap model for recall (top-100)
- Expensive reranker for precision (top-10)
- Reduces costs while maintaining quality

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Token limit exceeded | Truncate or chunk long texts |
| Wrong similarity metric | Use cosine for unnormalized, dot product for normalized |
| Model mismatch | Query with same model used for indexing |
| No batching | Always batch API calls |
| Empty text handling | Filter empty strings (produce zero vectors) |
| Inconsistent preprocessing | Same cleaning for index and query |
| Fine-tuning without reindexing | Always reindex after fine-tuning |

## Performance Benchmarks

### Throughput (typical)

| Setup | Throughput |
|-------|------------|
| OpenAI API batch | ~1000 docs/sec |
| Local GPU (8GB) batch=32 | ~200-500 docs/sec |
| Local GPU (40GB) batch=512 | ~2000+ docs/sec |
| Sorted + optimized | ~950 docs/sec (40% less compute) |

### Latency Targets

| Tier | Latency | Use Case |
|------|---------|----------|
| Hot cache (Redis) | <20ms | Real-time search |
| Warm cache (vector DB) | <50ms | Production search |
| Cold (API call) | 100-300ms | First-time queries |

## Sources

- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [Cohere Embed API](https://docs.cohere.com/reference/embed)
- [Voyage AI Documentation](https://docs.voyageai.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)
- [Top Embedding Models 2026](https://artsmart.ai/blog/top-embedding-models-in-2025/)
- [Embedding Models Comparison](https://research.aimultiple.com/embedding-models/)
- [Semantic Caching Patterns](https://www.dataquest.io/blog/semantic-caching-and-memory-patterns-for-vector-databases/)
- [Large-Scale Embedding Generation](https://blog.skypilot.co/large-scale-embedding/)
- [Token-Based Batching](https://www.mongodb.com/company/blog/engineering/token-count-based-batching-faster-cheaper-embedding-inference-for-queries)
