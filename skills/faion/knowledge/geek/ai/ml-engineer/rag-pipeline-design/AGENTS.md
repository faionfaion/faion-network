# RAG Pipeline Design

## Summary

Production RAG pipelines ground LLM responses in domain-specific data through a retrieval layer (embedding + vector search + reranking) followed by synthesis. Use hybrid search (vector + BM25) as the default; it improves recall@10 by 15-25% over pure vector search. Choose the architecture tier — Naive, Advanced, Modular, or Agentic — based on query complexity and data source heterogeneity.

## Why

LLMs hallucinate on private or recent knowledge. RAG solves this by retrieving relevant passages at query time and injecting them into context with source citations. Hybrid search, semantic chunking, and reranking are the three highest-impact improvements over a naive implementation. Retrieval quality (recall@10 >85%) must be measured before deploying — the ragas framework provides automated faithfulness and relevancy evaluation.

## When To Use

- LLM needs access to private, domain-specific, or frequently updated knowledge
- Application requires citations for user trust and verification
- Knowledge base exceeds the model's context window (>200K tokens of documents)
- Multiple heterogeneous data sources (PDFs, SQL DB, APIs) need unified semantic search
- Answer accuracy on domain queries is below acceptable threshold with prompt engineering alone

## When NOT To Use

- Knowledge is fully covered by the model's training and does not change — prompt engineering suffices
- Retrieval latency >500ms is unacceptable and caching cannot compensate
- Corpus is fewer than 50 documents — include them all in the context window (simpler, often more accurate)
- Team lacks infra to maintain a vector database and embedding pipeline — use a managed RAG service
- Queries are always the same — pre-generate answers and cache them instead of building a pipeline

## Content

| File | What's inside |
|------|---------------|
| `content/01-architecture.xml` | Architecture tiers (Naive/Advanced/Modular/Agentic), component stack, vector DB selection, chunking matrix |
| `content/02-retrieval.xml` | Hybrid search, reranking, HyDE, parent-child chunking, metadata filtering, agentic retrieval loop |
| `content/03-production.xml` | Production checklist: caching layers, monitoring, security, cost management, evaluation with ragas |

## Templates

| File | Purpose |
|------|---------|
| `templates/rag-pipeline.py` | Production RAG with Qdrant: ingest + hybrid search + metadata filter (~50 lines) |
| `templates/prompt-rag.txt` | RAG system prompt enforcing citation and "don't know" fallback |
