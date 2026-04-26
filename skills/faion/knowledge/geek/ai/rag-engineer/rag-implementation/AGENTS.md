# RAG Implementation

## Summary

Complete production RAG pipeline: document loading (txt/md/pdf/directory), chunking (fixed-size, sentence, paragraph, semantic, Markdown-header), embedding, Chroma-backed vector storage, retrieval, query enhancement (expansion, HyDE, rewrite), and LLM generation with a strict "answer only from context" system prompt. The pipeline is implemented as a single `RAGPipeline` class with separate ingest and query paths.

## Why

A well-structured RAG pipeline decouples ingestion from retrieval so each stage can be debugged independently. The retrieval recall gate (top-K chunks must contain the answer) is the most common failure mode; chunking strategy, chunk size, and top-K are the three primary levers. Grounding generation with a strict system prompt that forbids off-context answers is the minimum required guard against hallucination.

## When To Use

- Building a question-answering system over proprietary documents (PDFs, Markdown, text)
- LLM needs to answer questions about data post-dating its training cutoff
- Reducing hallucinations by grounding generation in retrieved facts
- Products requiring citations or source attribution alongside answers
- Knowledge-base chatbots where answers must come only from a controlled corpus

## When NOT To Use

- Corpus changes faster than re-ingestion can keep up — design a streaming update strategy first
- Purely conversational queries with no factual grounding need — RAG adds latency and cost with no benefit
- Entire knowledge base fits in context window — just include it directly
- Structured data questions (revenue figures, counts) — SQL + function-calling beats RAG for tabular data

## Content

| File | What's inside |
|------|---------------|
| `content/01-pipeline.xml` | RAGPipeline class: ingest, retrieve, generate, query methods with key rules |
| `content/02-chunking.xml` | Fixed-size, sentence, paragraph, semantic, and Markdown-header chunking strategies |
| `content/03-query-enhancement.xml` | Query expansion, HyDE, and query rewrite patterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/rag_pipeline.py` | Full RAGPipeline: Document/Chunk/RetrievalResult dataclasses + DocumentLoader |
