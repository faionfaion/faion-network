# RAG (Retrieval-Augmented Generation)

> Connect LLMs to external knowledge bases for accurate, up-to-date responses with source citations.

## What is RAG?

RAG is a framework that augments LLMs with real-time access to external knowledge. Instead of relying solely on training data, the model retrieves relevant documents at query time, making responses more accurate, current, and verifiable.

```
Query → Retrieve Context → Augment Prompt → Generate Response → Cite Sources
```

## Core Components

| Component | Purpose | Key Technologies |
|-----------|---------|------------------|
| **Document Loader** | Ingest documents from various sources | LlamaIndex readers, LangChain loaders |
| **Chunker** | Split documents into retrievable units | Semantic, recursive, structure-aware |
| **Embedder** | Convert text to vector representations | OpenAI, Cohere, local models |
| **Vector Store** | Store and search embeddings | Qdrant, Pinecone, pgvector, Chroma |
| **Retriever** | Find relevant chunks for queries | Vector search, hybrid, reranking |
| **Generator** | Produce final response with context | GPT-4, Claude, Gemini, local LLMs |

## When to Use RAG

### RAG is Best For

| Use Case | Why RAG Works |
|----------|---------------|
| **Dynamic knowledge** | Information changes frequently (docs, policies, news) |
| **Proprietary data** | Company-specific knowledge not in training data |
| **Source attribution** | Users need to verify claims with citations |
| **Large knowledge bases** | Too much data to fit in context window |
| **Cost sensitivity** | Cheaper than fine-tuning, no retraining needed |
| **Multi-tenant systems** | Different knowledge bases per user/org |

### RAG vs Fine-Tuning Decision Matrix

| Factor | Choose RAG | Choose Fine-Tuning |
|--------|------------|-------------------|
| **Data changes** | Frequently (daily/weekly) | Rarely (monthly+) |
| **Knowledge type** | Factual, lookup-oriented | Behavioral, stylistic |
| **Budget** | Limited compute budget | Can afford training |
| **Latency tolerance** | Can accept retrieval overhead | Need fastest inference |
| **Explainability** | Need source citations | Output style matters |
| **Data volume** | Large corpus (100K+ docs) | Small dataset (<10K examples) |

### Hybrid Approach (RAFT)

Combine both when you need:
- Domain-specific language/terminology (fine-tuning)
- Access to current information (RAG)
- High accuracy on specialized tasks

```
Fine-tuned Model + RAG Retrieval = Best of Both Worlds
```

## Key Concepts

### 1. Chunking Strategies

| Strategy | Best For | Chunk Size |
|----------|----------|------------|
| **Fixed-size** | Simple documents | 512-1024 tokens |
| **Recursive** | Most applications (default) | 256-512 tokens |
| **Semantic** | Knowledge bases, technical docs | Variable |
| **Structure-aware** | Markdown, HTML, code | Preserves structure |
| **LLM-based** | High-value documents | Context-dependent |

**Key insight:** Chunk size trades off context preservation vs retrieval precision.

### 2. Retrieval Strategies

| Strategy | Description | When to Use |
|----------|-------------|-------------|
| **Vector search** | Semantic similarity | General Q&A |
| **Hybrid (BM25 + Vector)** | Combine keyword + semantic | Technical queries |
| **Multi-query** | Generate query variations | Complex questions |
| **Hierarchical** | Summary → Section → Chunk | Large document sets |
| **Auto-merging** | Return parent if many children match | Context-dependent answers |

### 3. Reranking

Always rerank for production:
- Initial retrieval: Broad recall (top-20)
- Reranking: Precise relevance (top-5)
- Models: `cross-encoder/ms-marco-MiniLM`, Cohere Rerank

### 4. Response Synthesis

| Mode | Description | Token Usage |
|------|-------------|-------------|
| **Compact** | Concatenate chunks, single LLM call | Efficient |
| **Refine** | Iteratively refine answer per chunk | Higher quality |
| **Tree summarize** | Hierarchical summarization | Large results |
| **Simple** | Direct context injection | Fastest |

## Architecture Patterns

### Basic RAG

```
User Query
    ↓
Embed Query
    ↓
Vector Search (top-k)
    ↓
Rerank Results
    ↓
Inject Context + Prompt
    ↓
LLM Generation
    ↓
Response with Citations
```

### Agentic RAG

```
User Query
    ↓
Agent Reasoning
    ↓
[Decision: Retrieve or Answer Directly?]
    ↓
If Retrieve:
    → Query Reformulation
    → Multi-source Retrieval
    → Tool Execution (SQL, API, etc.)
    ↓
Synthesize Response
    ↓
Self-evaluate & Iterate
```

### Long RAG

```
Documents (full or sections)
    ↓
Long-context Embedding
    ↓
Coarse Retrieval
    ↓
In-context Refinement (LLM)
    ↓
Response Generation
```

## Vector Database Selection

| Database | Best For | Key Features |
|----------|----------|--------------|
| **Qdrant** | Production self-hosted | Filtering, HNSW, Rust performance |
| **Pinecone** | Serverless, managed | Zero-ops, auto-scaling |
| **Weaviate** | Knowledge graphs | Hybrid search, modules |
| **pgvector** | PostgreSQL users | Familiar stack, ACID |
| **Chroma** | Local development | Simple, in-memory |
| **Milvus** | Large scale (1B+) | GPU support, distributed |

## Embedding Model Selection

| Model | Dimensions | Context | Best For |
|-------|------------|---------|----------|
| **text-embedding-3-large** | 3072 | 8191 | Production (OpenAI) |
| **text-embedding-3-small** | 1536 | 8191 | Cost-efficient |
| **voyage-3** | 1024 | 32000 | Long documents |
| **bge-large-en-v1.5** | 1024 | 512 | Local/self-hosted |
| **all-MiniLM-L6-v2** | 384 | 256 | Fast, lightweight |

## LLM Usage Tips

### Prompting for RAG

1. **Be explicit about sources**: "Answer ONLY based on the provided context"
2. **Require citations**: "Cite sources using [Source: filename] format"
3. **Handle uncertainty**: "If the context doesn't contain the answer, say so"
4. **Avoid hallucination**: "Do not make up information not in the context"

### Context Window Management

| Strategy | When to Use |
|----------|-------------|
| **Reduce top-k** | Context too long |
| **Increase chunk size** | Few chunks with complete ideas |
| **Contextual compression** | Summarize retrieved docs |
| **Metadata filtering** | Pre-filter irrelevant docs |

### Cost Optimization

- Cache frequent queries and embeddings
- Use smaller embedding models for prototyping
- Batch embedding requests
- Filter by metadata before vector search
- Use local models for development

## Evaluation Metrics

### Retrieval Quality

| Metric | Description | Target |
|--------|-------------|--------|
| **Recall@k** | Relevant docs in top-k | > 0.8 |
| **MRR** | Rank of first relevant doc | > 0.7 |
| **NDCG** | Ranking quality overall | > 0.7 |

### Generation Quality

| Metric | Description | Target |
|--------|-------------|--------|
| **Faithfulness** | Answer grounded in context | > 0.9 |
| **Answer Relevancy** | Answer addresses query | > 0.8 |
| **Context Precision** | Retrieved docs are useful | > 0.7 |
| **Context Recall** | All needed info retrieved | > 0.8 |

## Common Failure Modes

| Problem | Cause | Solution |
|---------|-------|----------|
| **Empty results** | Query too specific | Query expansion, lower threshold |
| **Irrelevant results** | Poor chunking | Adjust chunk size, add overlap |
| **Hallucinations** | Insufficient context | Stricter prompts, more chunks |
| **Slow queries** | Large index, no filters | Metadata filtering, reduce top-k |
| **Contradictions** | Outdated documents | Version control, date filtering |

## Files in This Folder

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Step-by-step implementation checklists |
| [examples.md](examples.md) | Real-world architectures and code |
| [templates.md](templates.md) | RAG pipeline and prompt templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for building RAG systems |

## External Resources

### Official Documentation

- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- [LangChain RAG Tutorial](https://docs.langchain.com/oss/python/langchain/rag)
- [RAGAS Evaluation](https://docs.ragas.io/)

### Best Practices Guides

- [LlamaIndex Production RAG](https://developers.llamaindex.ai/python/framework/optimizing/production_rag/)
- [The Ultimate RAG Blueprint 2025/2026](https://langwatch.ai/blog/the-ultimate-rag-blueprint-everything-you-need-to-know-about-rag-in-2025-2026)
- [RAG Architecture Explained 2025](https://orq.ai/blog/rag-architecture)

### Research & Deep Dives

- [Comprehensive RAG Survey (arXiv)](https://arxiv.org/html/2506.00054v1)
- [Enhancing RAG Best Practices (arXiv)](https://arxiv.org/abs/2501.07391)
- [RAG vs Fine-Tuning (IBM)](https://www.ibm.com/think/topics/rag-vs-fine-tuning)

### Chunking Strategies

- [Weaviate Chunking Strategies](https://weaviate.io/blog/chunking-strategies-for-rag)
- [Best Chunking Strategies 2025](https://www.firecrawl.dev/blog/best-chunking-strategies-rag-2025)
- [11 Chunking Strategies Visualized](https://masteringllm.medium.com/11-chunking-strategies-for-rag-simplified-visualized-df0dbec8e373)

### Evaluation

- [RAG Evaluation Guide (Qdrant)](https://qdrant.tech/blog/rag-evaluation-guide/)
- [RAG Evaluation Metrics (Confident AI)](https://www.confident-ai.com/blog/rag-evaluation-metrics-answer-relevancy-faithfulness-and-more)
- [Complete RAG Evaluation Guide (Evidently AI)](https://www.evidentlyai.com/llm-guide/rag-evaluation)

### Tools & Frameworks

- [Qdrant Vector Database](https://qdrant.tech/)
- [Pinecone](https://www.pinecone.io/)
- [Weaviate](https://weaviate.io/)
- [ChromaDB](https://www.trychroma.com/)

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [faion-rag-engineer](../../faion-rag-engineer/CLAUDE.md) | Specialized RAG skill |
| [faion-llm-integration](../../faion-llm-integration/CLAUDE.md) | LLM APIs for generation |
| [faion-ai-agents](../../faion-ai-agents/CLAUDE.md) | Agentic RAG patterns |

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Embedding selection | sonnet | Vector model choice |
| Vector DB setup | haiku | Database configuration |
| Retrieval optimization | sonnet | Performance tuning |
| RAG pipeline design | opus | Architecture decisions |
