# Reranking for RAG Systems

Reranking is a second-stage retrieval technique that refines initial search results using more sophisticated models. While first-stage retrieval prioritizes speed (bi-encoders), reranking uses slower but more accurate cross-encoders to improve result quality.

**Key benefit:** Cross-encoder reranking improves RAG accuracy by 20-35% while adding 200-500ms latency per query.

## Table of Contents

- [When to Use Reranking](#when-to-use-reranking)
- [Key Concepts](#key-concepts)
- [Model Comparison](#model-comparison)
- [Architecture Patterns](#architecture-patterns)
- [Performance Benchmarks](#performance-benchmarks)
- [Integration Considerations](#integration-considerations)
- [External Resources](#external-resources)

---

## When to Use Reranking

### High-Value Use Cases

| Use Case | Why Reranking Helps |
|----------|---------------------|
| Legal document search | Precision critical; mistakes costly |
| Medical Q&A systems | Wrong answer can harm patients |
| Enterprise RAG | Domain-specific relevance needed |
| Customer support | Accurate answers reduce escalation |
| Code search | Semantic matching > keyword matching |
| E-commerce search | Better relevance drives conversions |

### Decision Matrix

| Scenario | Reranking Needed? | Reason |
|----------|-------------------|--------|
| Initial retrieval quality poor | Yes | Reranker refines noisy results |
| Hybrid search fusion | Yes | Balance BM25 + dense scores |
| Latency budget < 100ms | No | Reranking adds 100-500ms |
| < 10 documents retrieved | Maybe | Limited improvement potential |
| Multi-hop reasoning | Yes | Quality matters more than speed |
| Real-time autocomplete | No | Too slow for interactive use |

### Prerequisites for Effective Reranking

1. **Sufficient candidate pool** - Retrieve 3-10x more candidates than final top-k
2. **Reasonable first-stage recall** - Reranker cannot recover missing documents
3. **Latency budget** - Allow 100-500ms additional processing time
4. **Quality-sensitive application** - Improvement justifies added complexity

---

## Key Concepts

### Two-Stage Retrieval Architecture

```
Stage 1: RETRIEVAL (Fast, ~10ms)
Query → Bi-Encoder → Vector Search → Top 50-100 candidates

Stage 2: RERANKING (Slow, ~100-500ms)
(Query, Doc) pairs → Cross-Encoder → Top 5-10 reranked results
```

### Bi-Encoder vs Cross-Encoder

| Aspect | Bi-Encoder | Cross-Encoder |
|--------|------------|---------------|
| **Architecture** | Separate encoders for Q and D | Joint encoder for (Q, D) pair |
| **Speed** | Fast (~10ms for 1M docs) | Slow (~100-500ms for 50 docs) |
| **Accuracy** | Good (70-80% nDCG) | Excellent (85-95% nDCG) |
| **Precomputation** | Yes (store doc embeddings) | No (compute at query time) |
| **Scalability** | Excellent (ANN search) | Poor (O(n) pairs) |
| **Use case** | First-stage retrieval | Second-stage reranking |

### Why Cross-Encoders Are More Accurate

1. **Full attention** - Query and document tokens attend to each other
2. **No compression loss** - Bi-encoders compress meaning into single vector
3. **Context-aware** - Can match query terms in document context
4. **Fine-grained matching** - Token-level relevance signals

### Reranking Architectures

| Architecture | Description | Latency | Accuracy |
|--------------|-------------|---------|----------|
| **Pointwise** | Score each (Q, D) pair independently | Medium | Good |
| **Pairwise** | Compare document pairs for ranking | High | Better |
| **Listwise** | Consider all documents together | High | Best |
| **Late Interaction** | Token-level scoring (ColBERT) | Low | Good |

---

## Model Comparison

### Top Reranking Models (2025-2026)

| Model | Parameters | BEIR nDCG@10 | Languages | License |
|-------|------------|--------------|-----------|---------|
| **Jina Reranker v3** | 0.6B | 61.94 | 100+ | Apache 2.0 |
| **Cohere Rerank 3** | Unknown | ~60 | 100+ | Proprietary |
| **Cohere Rerank 3 Nimble** | Unknown | ~58 | 100+ | Proprietary |
| **BGE Reranker v2-M3** | 0.6B | ~59 | 100+ | Apache 2.0 |
| **BGE Layerwise (Gemma)** | 2B+ | ~62 | Multiple | Apache 2.0 |
| **Mixedbread mxbai-rerank-large** | 0.4B | ~58 | English | Apache 2.0 |
| **MS MARCO MiniLM-L12** | 33M | ~52 | English | MIT |
| **Pinecone Rerank V0** | Unknown | ~57 | English | Proprietary |
| **ZeroEntropy zerank-1** | Unknown | +28% vs baseline | Multiple | Proprietary |

### Model Selection Guide

#### By Use Case

| Use Case | Recommended Model | Reason |
|----------|-------------------|--------|
| Production RAG (English) | Cohere Rerank 3 Nimble | Fast, accurate, managed |
| Multilingual production | Jina Reranker v3 | Best multilingual, SOTA |
| Self-hosted (open source) | BGE Reranker v2-M3 | Apache 2.0, excellent quality |
| Low latency required | MS MARCO MiniLM-L6 | Smallest, fastest |
| Maximum accuracy | BGE Layerwise (Gemma) | SOTA but slow |
| Cost-sensitive | FlashRank | Lightweight, free |

#### By Infrastructure

| Infrastructure | Recommended Model |
|----------------|-------------------|
| GPU available | BGE Reranker v2-M3, Jina v3 |
| CPU only | MS MARCO MiniLM, FlashRank |
| Serverless / no infra | Cohere, Pinecone APIs |
| Air-gapped environment | Any open-source model |

### Detailed Model Profiles

#### Jina Reranker v3

- **Architecture:** Novel "Last but Not Late Interaction" (LBNL)
- **Parameters:** 0.6B (10x smaller than generative listwise rerankers)
- **Strengths:**
  - SOTA BEIR performance (61.94 nDCG@10)
  - Excellent multi-hop retrieval (78.56 on HotpotQA)
  - Outstanding fact verification (93.95 on FEVER)
  - 100+ languages supported
- **Best for:** Multilingual production, complex reasoning queries

#### Cohere Rerank 3

- **Architecture:** Transformer-based cross-encoder
- **Variants:** Standard (accurate) and Nimble (fast)
- **Strengths:**
  - 100+ languages
  - Easy API integration
  - No infrastructure management
  - Production-ready with SLA
- **Best for:** Quick deployment, managed solution

#### BGE Reranker Series

- **Variants:**
  - `bge-reranker-v2-m3`: 0.6B params, multilingual
  - `bge-reranker-large`: Larger English model
  - `bge-layerwise-gemma/minicpm`: LLM-based, SOTA accuracy
- **Strengths:**
  - Open source (Apache 2.0)
  - Self-hostable
  - Multiple size options
- **Best for:** Self-hosted production, cost control

#### MS MARCO Cross-Encoders

- **Variants:**
  - `ms-marco-MiniLM-L-6-v2`: 22M params, fastest
  - `ms-marco-MiniLM-L-12-v2`: 33M params, balanced
  - `ms-marco-electra-base`: 110M params, most accurate
- **Strengths:**
  - Tiny, fast
  - Well-tested baseline
  - MIT license
- **Best for:** Development, low-resource environments

---

## Architecture Patterns

### Pattern 1: Simple Two-Stage Retrieval

```
Query
  │
  ▼
[Bi-Encoder] → Embed query
  │
  ▼
[Vector DB] → Retrieve top-50
  │
  ▼
[Cross-Encoder] → Rerank to top-5
  │
  ▼
[LLM] → Generate answer
```

**When to use:** Standard RAG applications

### Pattern 2: Hybrid Search + Reranking

```
Query
  │
  ├─────────────┬─────────────┐
  ▼             ▼             ▼
[BM25]      [Dense]      [Sparse]
  │             │             │
  └─────────────┴─────────────┘
                │
                ▼
         [RRF Fusion] → Top-100
                │
                ▼
         [Cross-Encoder] → Top-10
                │
                ▼
              [LLM]
```

**When to use:** Documents have keyword-heavy content (code, technical docs)

### Pattern 3: Multi-Stage Reranking

```
Query
  │
  ▼
[First Stage] → Top-1000 (BM25 or vector)
  │
  ▼
[Light Reranker] → Top-100 (MiniLM-L6)
  │
  ▼
[Heavy Reranker] → Top-10 (BGE or Cohere)
  │
  ▼
[LLM]
```

**When to use:** Large corpus, need both speed and accuracy

### Pattern 4: Diverse Reranking (MMR)

```
Query
  │
  ▼
[Cross-Encoder] → Score all candidates
  │
  ▼
[MMR Selection] → Balance relevance + diversity
  │
  ▼
Top-k diverse results
```

**When to use:** Results too similar, need coverage

---

## Performance Benchmarks

### Latency Expectations

| Model | Hardware | Documents | Latency |
|-------|----------|-----------|---------|
| MiniLM-L6 | CPU | 50 | 50-100ms |
| MiniLM-L12 | CPU | 50 | 100-200ms |
| BGE v2-M3 | GPU | 50 | 50-100ms |
| Jina v3 | GPU | 50 | 100-150ms |
| Cohere API | N/A | 50 | 200-400ms |

### Quality Improvements

| Scenario | Without Reranking | With Reranking | Improvement |
|----------|-------------------|----------------|-------------|
| Generic RAG | 65% nDCG@10 | 82% nDCG@10 | +26% |
| Legal search | 58% recall@5 | 78% recall@5 | +34% |
| Code search | 52% MRR | 71% MRR | +37% |

### Optimal Candidate Pool Sizes

| Application Type | Retrieve | Rerank to | Reason |
|------------------|----------|-----------|--------|
| Chat/RAG | 50 | 5-10 | Speed matters |
| Document search | 100-200 | 10-20 | Comprehensive results |
| Legal/medical | 100-200 | 5 | Precision critical |
| E-commerce | 50-75 | 10-15 | Balance quality/speed |

---

## Integration Considerations

### API-Based Rerankers

**Pros:**
- No infrastructure management
- Automatic updates
- Production SLAs

**Cons:**
- Per-request costs
- Network latency
- Data leaves your infrastructure

**Providers:**
- Cohere Rerank API
- Jina AI API
- Pinecone Rerank
- ZeroEntropy

### Self-Hosted Rerankers

**Pros:**
- No per-request costs
- Data stays in-house
- Full control

**Cons:**
- Infrastructure management
- GPU costs
- Model updates manual

**Options:**
- Sentence Transformers (Python)
- Hugging Face Transformers
- AnswerDotAI rerankers library

### Hybrid Approach

Use API for:
- Production traffic
- Spiky workloads
- Quick deployment

Use self-hosted for:
- High-volume applications
- Sensitive data
- Cost optimization

---

## External Resources

### Official Documentation

- [Cohere Rerank API](https://docs.cohere.com/docs/reranking)
- [Jina Reranker v3](https://jina.ai/models/jina-reranker-v3/)
- [BGE Rerankers (BAAI)](https://huggingface.co/BAAI)
- [Sentence Transformers Cross-Encoders](https://www.sbert.net/examples/applications/cross-encoder/README.html)
- [AnswerDotAI rerankers](https://github.com/AnswerDotAI/rerankers)

### Benchmarks & Research

- [BEIR Benchmark](https://github.com/beir-cellar/beir)
- [MS MARCO Dataset](https://microsoft.github.io/msmarco/)
- [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)
- [Pinecone Rerankers Guide](https://www.pinecone.io/learn/series/rag/rerankers/)

### Research Papers

- [Jina-Reranker-V3: Last but Not Late Interaction](https://arxiv.org/html/2509.25085v2)
- [ColBERT: Efficient and Effective Passage Search](https://arxiv.org/abs/2004.12832)
- [Maximal Marginal Relevance (MMR)](https://www.cs.cmu.edu/~jgc/publication/The_Use_MMR_Diversity_Based_LTMIR_1998.pdf)

### Tutorials & Guides

- [Ultimate Guide to Choosing Reranking Models 2025](https://www.zeroentropy.dev/articles/ultimate-guide-to-choosing-the-best-reranking-model-in-2025)
- [Top 7 Rerankers for RAG](https://www.analyticsvidhya.com/blog/2025/06/top-rerankers-for-rag/)
- [LlamaIndex Reranking Guide](https://www.llamaindex.ai/blog/boosting-rag-picking-the-best-embedding-reranker-models-42d079022e83)
- [Zilliz Rerankers Tutorial](https://zilliz.com/learn/what-are-rerankers-enhance-information-retrieval)

### API Providers Comparison

- [Agentset Reranker Leaderboard](https://agentset.ai/rerankers)
- [SiliconFlow API Providers Guide](https://www.siliconflow.com/articles/en/the-best-api-providers-of-open-source-reranker-model)

---

## Related Files

| File | Description |
|------|-------------|
| [checklist.md](checklist.md) | Selection & implementation checklists |
| [examples.md](examples.md) | Code examples with different models |
| [templates.md](templates.md) | Pipeline & configuration templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for debugging & optimization |
