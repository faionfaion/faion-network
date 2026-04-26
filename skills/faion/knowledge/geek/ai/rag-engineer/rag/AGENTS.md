# RAG Pipeline

## Summary

A Retrieval-Augmented Generation pipeline ingests documents (load → chunk → embed → store), retrieves relevant chunks for a query (embed → vector search → rerank), and generates a grounded answer with source citations. The reference stack uses LlamaIndex + Qdrant + cross-encoder reranking + RAGAS evaluation. Key invariants: chunk quality bounds retrieval quality; hybrid search is the default; reranking is required for production accuracy; evaluate with MRR > 0.7 and faithfulness > 0.9 before launch.

## Why

LLMs hallucinate on domain-specific or frequently-updated knowledge not in their training data. RAG grounds answers in a retrievable document corpus and surfaces citations, enabling compliance and user trust. A structured pipeline (ingest → retrieve → rerank → generate) separates the concerns that most commonly break: bad chunking, stale indexes, missing metadata, and context overflow.

## When To Use

- Agent needs to answer questions grounded in a private or frequently-updated document corpus.
- Reducing hallucinations on domain-specific topics not in the model's training data.
- Building a knowledge assistant over PDFs, docs, wikis, or code repositories.
- Source corpus is too large to fit in a single context window.
- Citation / source attribution is required for compliance or user trust.

## When NOT To Use

- Document set is tiny (< 50 chunks) and fits in context — just stuff the full context.
- Questions are purely general knowledge — RAG adds retrieval latency with no accuracy gain.
- Real-time data (stock prices, live APIs) — RAG retrieves static indexed content; use live tool calls.
- Query volume is very low and latency is critical — embed + retrieve round-trip adds 200–600ms.

## Content

| File | What's inside |
|------|---------------|
| `content/01-ingestion.xml` | Document loading, chunking strategy by document type, metadata requirements, deduplication. |
| `content/02-retrieval.xml` | Semantic search, hybrid search default, reranking rules, top_k x chunk_size budget constraint. |
| `content/03-generation.xml` | RAG prompt pattern, faithfulness constraint, citation format, faithfulness post-check. |
| `content/04-evaluation.xml` | RAGAS metrics (MRR, faithfulness, answer relevance), production checklist thresholds. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rag-query.py` | Minimal RAG query with reranking using LlamaIndex + SentenceTransformerRerank. |
| `templates/rag-prompt.txt` | System + context prompt template enforcing "answer only from context" with citation format. |
