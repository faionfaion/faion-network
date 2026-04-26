# RAG (Retrieval-Augmented Generation)

## Summary

A framework for augmenting LLMs with real-time access to external knowledge: embed query → retrieve top-k chunks from vector store → rerank to top-5 → inject context into prompt → generate with citations. Always rerank (retrieve top-20, reduce to top-5); always include a "no information" path when retrieval fails; always include source metadata in chunks for citations.

## Why

LLMs cannot answer questions about documents not in their training data, and hallucinate when asked to recall private or recent information. RAG grounds responses in retrieved evidence, enables source citation, and scales to large corpora without retraining. It is substantially cheaper than fine-tuning for factual recall tasks.

## When To Use

- Application needs answers about documents not in training data
- Knowledge is updated frequently (daily/weekly) and retraining is impractical
- Users need source citations to verify claims
- Knowledge base is too large for a single context window (hundreds+ of pages)
- Multi-tenant system where each tenant has a separate knowledge base
- Cost constraint: RAG is substantially cheaper than fine-tuning for factual recall

## When NOT To Use

- Knowledge is behavioral (writing style, persona, domain jargon) — use fine-tuning
- Corpus is fewer than 50 documents that fit in a single long-context prompt — skip retrieval
- Latency budget is under 200ms — retrieval + reranking adds 100-500ms overhead
- Task is pure reasoning on data already in the prompt — retrieval introduces noise

## Content

| File | What's inside |
|------|---------------|
| `content/01-pipeline.xml` | Core pipeline stages, chunking strategies, retrieval strategies, reranking rule |
| `content/02-evaluation.xml` | RAGAS metrics, retrieval quality thresholds, generation quality thresholds, evaluation cadence |
| `content/03-gotchas.xml` | Failure modes: retrieval miss, prompt injection, index drift, hallucination on insufficient context |

## Templates

| File | Purpose |
|------|---------|
| `templates/rag-pipeline.py` | Production RAG skeleton: ingest → index → query with reranking (LlamaIndex) |
| `templates/rag-prompt.txt` | RAG generation prompt: source-only constraint, citation format, "I don't know" handling |
