# Text Embeddings Guide

Comprehensive guide for selecting, implementing, and optimizing text embeddings for semantic search, RAG, and similarity tasks.

---

## What Are Text Embeddings?

Text embeddings are dense vector representations that capture semantic meaning of text. Similar texts have vectors that are close together in the embedding space, enabling:

- **Semantic search** - Find relevant documents beyond keyword matching
- **RAG (Retrieval-Augmented Generation)** - Ground LLM responses in relevant context
- **Clustering** - Group similar documents automatically
- **Classification** - Categorize text based on learned representations
- **Anomaly detection** - Identify outliers in document collections

---

## Model Comparison (2025-2026)

### Proprietary Models

| Model | Provider | Dimensions | Max Tokens | Cost/1M tokens | MTEB Score | Best For |
|-------|----------|------------|------------|----------------|------------|----------|
| **text-embedding-3-large** | OpenAI | 256-3072 | 8191 | $0.13 | 64.6% | Production RAG, high quality |
| **text-embedding-3-small** | OpenAI | 256-1536 | 8191 | $0.02 | 62.3% | Cost-sensitive apps |
| **voyage-4-large** | Voyage AI | 256-2048 | 32K | $0.12 | ~68% | SOTA retrieval, MoE |
| **voyage-3.5** | Voyage AI | 256-2048 | 32K | $0.06 | ~66% | Best price/quality |
| **voyage-context-3** | Voyage AI | 1024 | 32K | $0.06 | - | Contextualized chunks |
| **embed-v4** | Cohere | 256-1536 | 128K | $0.10 | ~65% | Multimodal, long docs |
| **embed-multilingual-v3.0** | Cohere | 1024 | 512 | $0.10 | - | 100+ languages |
| **mistral-embed** | Mistral | 1024 | 8192 | $0.10 | 77.8%* | High accuracy |

*Accuracy metric, not MTEB average

### Open-Source Models

| Model | Dimensions | Max Tokens | MTEB Score | Speed | Best For |
|-------|------------|------------|------------|-------|----------|
| **BGE-M3** | 1024 | 8192 | 68.1% | Slow | Best quality, hybrid search |
| **Qwen3-Embedding-0.6B** | 1024 | 8192 | ~67% | Medium | Instruction-aware |
| **nomic-embed-text-v2** | 768 | 8192 | ~66% | Fast | Long context, multilingual |
| **bge-large-en-v1.5** | 1024 | 512 | 63.6% | Medium | Balanced quality/speed |
| **e5-large-v2** | 1024 | 512 | ~64% | Medium | Semantic similarity |
| **gte-large** | 1024 | 512 | ~63% | Medium | General purpose |
| **all-MiniLM-L6-v2** | 384 | 256 | ~58% | Very Fast | Real-time, low latency |
| **EmbeddingGemma-300M** | 768 | 8192 | ~62% | Fast | On-device deployment |

---

## When to Use Which Model

### By Use Case

| Use Case | Recommended | Alternative | Why |
|----------|-------------|-------------|-----|
| **Production RAG** | voyage-3.5 | text-embedding-3-large | Best retrieval quality |
| **Cost-sensitive** | text-embedding-3-small | BGE-M3 (local) | Low cost, good quality |
| **Multilingual** | embed-v4 | BGE-M3 | 100+ languages |
| **Long documents** | voyage-context-3 | embed-v4 (128K) | Document-level context |
| **Code search** | voyage-code-3 | CodeBERT | Code-specific training |
| **Air-gapped/Private** | BGE-M3 | nomic-embed-text-v2 | No API calls |
| **Real-time search** | all-MiniLM-L6-v2 | nomic-embed-text-v2 | Sub-10ms latency |
| **Multimodal** | embed-v4 | CLIP | Images + text |
| **Legal/Finance** | voyage-3-large | voyage-finance-2 | Domain-specific |

### By Constraint

| Constraint | Recommendation |
|------------|----------------|
| **Budget < $100/month** | text-embedding-3-small + caching |
| **Latency < 10ms** | Local model (all-MiniLM-L6-v2) |
| **No external APIs** | BGE-M3 or nomic-embed-text-v2 |
| **GPU available** | BGE-M3 with FP16 |
| **CPU only** | all-MiniLM-L6-v2 or Model2Vec |
| **Massive scale (100M+ docs)** | Quantized voyage-3.5 (int8) |

---

## Key Features Comparison

### Matryoshka Embeddings (Dimension Reduction)

Native dimension reduction without retraining:

| Model | Supported Dimensions | Quality Loss at 256d |
|-------|---------------------|---------------------|
| text-embedding-3-large | 256, 512, 1024, 1536, 3072 | ~4% |
| voyage-3.5 | 256, 512, 1024, 2048 | ~3% |
| embed-v4 | 256, 512, 1024, 1536 | ~3% |
| nomic-embed-text-v2 | 64, 128, 256, 512, 768 | ~5% |

### Quantization Support

| Model | Float32 | Float16 | INT8 | Binary |
|-------|---------|---------|------|--------|
| voyage-3.5 | Yes | Yes | Yes | Yes |
| embed-v4 | Yes | Yes | Yes | No |
| text-embedding-3-large | Yes | No | No | No |
| BGE-M3 | Yes | Yes | Yes | Yes |

### Input Types (Cohere-style)

| Provider | Document | Query | Classification | Clustering |
|----------|----------|-------|----------------|------------|
| Cohere | search_document | search_query | classification | clustering |
| Voyage AI | document | query | - | - |
| OpenAI | - | - | - | - |

---

## LLM Usage Tips

### For RAG Systems

1. **Use asymmetric embeddings** when available (Cohere, Voyage)
   - Embed documents with `input_type="document"`
   - Embed queries with `input_type="query"`

2. **Chunk strategically**
   - Q&A: 256-512 tokens
   - Summarization: 1000-2000 tokens
   - Code: 100-200 tokens with 50% overlap

3. **Consider hybrid search**
   - Combine dense embeddings with BM25
   - BGE-M3 provides both dense and sparse

4. **Use reranking**
   - First pass: cheap/fast embeddings (top 100)
   - Second pass: reranker for precision (top 10)

### For Cost Optimization

1. **Batch requests** - Up to 10x cost reduction
2. **Cache aggressively** - 80% cache hit = 80% savings
3. **Use dimension reduction** - 256d is often sufficient
4. **Deduplicate before embedding** - TF-IDF similarity > 0.95 = skip
5. **Quantize vectors** - INT8 reduces storage 4x with <1% quality loss

### For Quality Optimization

1. **Benchmark on YOUR data** - MTEB scores are general
2. **Fine-tune when needed** - Adapter layers for domain data
3. **Contextualize chunks** - voyage-context-3 or prepend metadata
4. **Evaluate with real queries** - Not synthetic benchmarks

---

## Provider-Specific Notes

### OpenAI

- **Strengths**: Simple API, good quality, native dimension reduction
- **Weaknesses**: No input types, no quantization, no local option
- **Best models**: text-embedding-3-large (quality), text-embedding-3-small (cost)
- **Batching**: Up to 2048 texts per request

### Voyage AI (MongoDB)

- **Strengths**: SOTA quality, shared embedding space, MoE architecture
- **Weaknesses**: Newer ecosystem, limited enterprise integrations
- **Best models**: voyage-4-large (quality), voyage-3.5 (balanced)
- **Special**: voyage-context-3 for contextualized chunks

### Cohere

- **Strengths**: Multimodal (embed-v4), 128K context, mature API
- **Weaknesses**: Higher latency, complex pricing
- **Best models**: embed-v4 (multimodal), embed-multilingual-v3.0 (languages)
- **Special**: Input types for asymmetric search

### Local (sentence-transformers)

- **Strengths**: Free, private, customizable, GPU acceleration
- **Weaknesses**: Requires infrastructure, slower than APIs (usually)
- **Best models**: BGE-M3 (quality), all-MiniLM-L6-v2 (speed)
- **Special**: 15,000+ pre-trained models on HuggingFace

---

## Decision Framework

```
START
  |
  v
Need multimodal (images)?
  |
  Yes --> embed-v4 (Cohere)
  |
  No
  v
Need >8K token context?
  |
  Yes --> embed-v4 (128K) or voyage-context-3
  |
  No
  v
Can use external API?
  |
  No --> BGE-M3 (quality) or all-MiniLM-L6-v2 (speed)
  |
  Yes
  v
Budget > $500/month?
  |
  No --> text-embedding-3-small + caching
  |
  Yes
  v
Need SOTA retrieval?
  |
  Yes --> voyage-3.5 or voyage-4-large
  |
  No --> text-embedding-3-large
```

---

## Benchmarking Your Use Case

MTEB scores are general benchmarks. Always benchmark on your specific data:

1. **Create evaluation set** - 100-500 query-document pairs
2. **Test multiple models** - At least 3-4 candidates
3. **Measure what matters**:
   - Recall@10 for RAG
   - MRR for search ranking
   - Precision@K for filtering
4. **Consider operational costs**:
   - API costs per 1M tokens
   - Latency p50/p95
   - Storage per document

---

## External References

### Official Documentation

- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [Voyage AI Documentation](https://docs.voyageai.com/docs/embeddings)
- [Cohere Embed Guide](https://docs.cohere.com/docs/cohere-embed)
- [Sentence Transformers](https://sbert.net/)
- [HuggingFace MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)

### Research Papers

- [Matryoshka Representation Learning](https://arxiv.org/abs/2205.13147)
- [BGE-M3 Paper](https://arxiv.org/abs/2402.03216)
- [Text Embeddings Reveal (Almost) As Much As Text](https://arxiv.org/abs/2310.06816)

### Tutorials and Guides

- [Pinecone Chunking Strategies](https://www.pinecone.io/learn/chunking-strategies/)
- [LlamaIndex Embedding Guide](https://docs.llamaindex.ai/en/stable/module_guides/models/embeddings/)
- [LangChain Text Embeddings](https://python.langchain.com/docs/modules/data_connection/text_embedding/)

### Model Hubs

- [HuggingFace Sentence Transformers](https://huggingface.co/sentence-transformers)
- [BAAI BGE Models](https://huggingface.co/BAAI)
- [Nomic AI Models](https://huggingface.co/nomic-ai)

---

## Related Files

| File | Description |
|------|-------------|
| [checklist.md](checklist.md) | Implementation and evaluation checklists |
| [examples.md](examples.md) | Code examples for all providers |
| [templates.md](templates.md) | Reusable embedding pipeline templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for model selection and debugging |

---

*Last updated: January 2026*
*Sources: [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard), [Voyage AI Blog](https://blog.voyageai.com/), [Cohere Docs](https://docs.cohere.com/), [OpenAI Docs](https://platform.openai.com/docs/)*
