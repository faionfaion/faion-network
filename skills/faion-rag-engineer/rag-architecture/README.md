---
id: rag-architecture
name: "RAG Architecture"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# RAG Architecture

## Overview

Retrieval Augmented Generation (RAG) combines information retrieval with LLM generation to produce accurate, grounded responses. This guide covers architecture patterns and design decisions.

## When to Use

- Question answering over custom documents
- Chatbots with domain-specific knowledge
- Document search and summarization
- Reducing LLM hallucinations
- When data changes frequently
- Cost-effective alternative to fine-tuning

## Architecture Patterns

### Basic RAG Flow

```
INDEXING PIPELINE
Documents → Chunking → Embedding → Vector Store

QUERY PIPELINE
Query → Embedding → Retrieval → Context → LLM → Response
```

### Pipeline Stages

| Stage | Purpose | Key Decisions |
|-------|---------|---------------|
| Ingestion | Load documents | File types, sources |
| Chunking | Split into pieces | Strategy, size, overlap |
| Embedding | Vectorize chunks | Model, dimensions |
| Indexing | Store vectors | Vector DB, index type |
| Retrieval | Find relevant chunks | Top-k, filtering |
| Generation | Produce response | Model, prompt design |

## Chunking Strategies

### Fixed Size
- **Use for:** General text, mixed content
- **Pros:** Simple, predictable
- **Cons:** May split context
- **Settings:** 500 chars, 50 overlap

### Sentence-Based
- **Use for:** Narrative text, articles
- **Pros:** Natural boundaries
- **Cons:** Variable size
- **Settings:** Max 500 chars, min 100 chars

### Paragraph-Based
- **Use for:** Structured documents
- **Pros:** Semantic units
- **Cons:** Large variance
- **Settings:** Max 1000 chars

### Semantic Chunking
- **Use for:** High-quality retrieval
- **Pros:** Context-aware splits
- **Cons:** Slow, expensive
- **Settings:** 0.8 similarity threshold

### Header-Based (Markdown)
- **Use for:** Documentation, structured MD
- **Pros:** Preserves structure
- **Cons:** Size variance
- **Settings:** Split by #, ##, ###

## Retrieval Strategies

### Basic Retrieval
- Embed query → find top-k similar chunks
- **Settings:** top_k=5, cosine similarity

### Hybrid Search
- Combine vector + keyword search
- **Best for:** Exact match + semantic
- **Settings:** 70% vector, 30% BM25

### Reranking
- Retrieve top-20 → rerank → return top-5
- **Best for:** High precision needs
- **Models:** Cohere rerank, cross-encoders

### Query Enhancement

| Method | Use Case | Benefit |
|--------|----------|---------|
| Query expansion | Vague questions | Better recall |
| HyDE (hypothetical answer) | Abstract questions | Better semantic match |
| Query rewriting | Ambiguous questions | Clarity |

## Context Management

### Context Window Strategies

| Strategy | Max Chunks | Total Tokens | Use Case |
|----------|-----------|--------------|----------|
| Minimal | 3 | 1500 | Simple Q&A |
| Standard | 5 | 2500 | General RAG |
| Rich | 10 | 5000 | Complex reasoning |
| Extended | 20 | 10000 | Research tasks |

### Context Ordering
1. **By relevance** - Most relevant first (default)
2. **By recency** - Newest first (time-sensitive)
3. **By source** - Group by document (navigation)

## Prompt Templates

### Default System Prompt
```
You are a helpful assistant that answers questions based on context.

Rules:
- Answer based ONLY on provided context
- If context doesn't contain answer, say "I don't have enough information"
- Be concise and accurate
```

### Technical Documentation
```
You are a technical documentation assistant.

Rules:
- Provide accurate, detailed technical answers
- Include code examples when relevant
- Reference specific documentation sections
- Explain technical concepts clearly
```

### Citation Style
```
You are a research assistant that provides cited answers.

Rules:
- Always cite sources using [Source: X] format
- Quote relevant passages when helpful
- Distinguish between direct quotes and paraphrasing
- Note when sources conflict
```

## Vector Database Selection

| Database | Best For | Deployment | Cost |
|----------|----------|------------|------|
| Qdrant | Production self-hosted | Docker | Free |
| Weaviate | Knowledge graphs | Kubernetes | Free |
| Chroma | Local dev, prototyping | Embedded | Free |
| pgvector | Existing PostgreSQL | Extension | Free |
| Pinecone | Fully managed | Cloud | $$$ |

### Qdrant (Recommended)
- High performance, cloud-native
- Rich filtering capabilities
- Production-ready
- Docker deployment

### Chroma (Development)
- Embedded database
- No external dependencies
- Perfect for prototyping
- Persistent or in-memory

## Quality Metrics

### Retrieval Quality
- **Recall@k** - Relevant docs in top-k
- **Precision@k** - Top-k are relevant
- **MRR** - Mean reciprocal rank
- **NDCG** - Normalized discounted cumulative gain

### Generation Quality
- **Faithfulness** - Response grounded in context
- **Relevance** - Answers the question
- **Completeness** - Covers key points
- **Conciseness** - Not overly verbose

### End-to-End
- **Accuracy** - Correct answers
- **Latency** - Response time
- **Cost** - API + DB costs
- **User satisfaction** - Feedback scores

## Best Practices

### Chunking
1. Match chunk size to question complexity
2. Use overlap (10-20%) to maintain context
3. Consider document structure
4. Test different strategies

### Retrieval
1. Start with more chunks (top-k=10), filter down
2. Use hybrid search (vector + keyword)
3. Implement reranking for precision
4. Cache embeddings for performance

### Context
1. Don't overwhelm LLM with too much context
2. Order chunks by relevance
3. Include source metadata
4. Remove duplicate information

### Prompts
1. Be explicit about using only provided context
2. Include instructions for handling missing info
3. Request citations when needed
4. Test with diverse questions

### Evaluation
1. Test with diverse questions
2. Measure retrieval and generation separately
3. Track faithfulness and relevance
4. Iterate based on metrics

## Common Pitfalls

| Pitfall | Impact | Solution |
|---------|--------|----------|
| Chunks too large | LLM can't focus | Reduce to 500 chars |
| Chunks too small | Loss of context | Increase to 300+ chars |
| Wrong embedding model | Poor retrieval | Match to use case |
| No overlap | Split information | Add 10-20% overlap |
| Ignoring metadata | Missing filters | Add source, date, type |
| Static top-k | Over/under retrieval | Adapt per query type |
| No reranking | Low precision | Add reranking step |

## Advanced Patterns

### Agentic RAG
- Agent decides when to retrieve
- Multiple retrieval rounds
- Dynamic query formulation

### Graph RAG
- Combine vector + knowledge graph
- Entity relationships
- Multi-hop reasoning

### Multi-Index RAG
- Separate indexes per domain
- Route queries to appropriate index
- Combine results from multiple sources

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Analyze and assess | sonnet | Evaluation and planning |
| Execute implementation | haiku | Apply established patterns |
| Review and validate | sonnet | Quality assurance |
| Strategic decision | opus | Novel scenarios |
| Optimize and refine | haiku | Performance tuning |
| Document approach | haiku | Create documentation |

## Sources

- [RAG Paper (Lewis et al.)](https://arxiv.org/abs/2005.11401)
- [LangChain RAG Tutorial](https://python.langchain.com/docs/tutorials/rag/)
- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- [Advanced RAG - Pinecone](https://www.pinecone.io/learn/advanced-rag-techniques/)
- [RAG Patterns](https://blog.llamaindex.ai/a-cheat-sheet-and-some-recipes-for-building-advanced-rag-803a9d94c41b)
