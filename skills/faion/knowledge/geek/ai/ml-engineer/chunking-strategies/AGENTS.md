# Chunking Strategies for RAG

## Summary

Chunking splits documents into semantically meaningful pieces for embedding and retrieval. The right strategy improves retrieval precision by 30-40%. Decision rule: if short (&lt;1000 tokens) → no chunking; if code → code-aware (AST); if structured (MD/HTML) → structure-based; if context-critical (legal/medical) → semantic; default → recursive with 15% overlap.

## Why

Embedding models have token limits; dense retrieval works better with focused content; and context windows waste tokens on irrelevant text. Over-compressed embeddings lose meaning. Chunk size and strategy directly determine whether the retriever can find the relevant passage — wrong chunking is the most common cause of RAG hallucinations from incomplete context.

## When To Use

- Building or improving a RAG ingestion pipeline where retrieval recall or precision is suboptimal
- Corpus contains mixed document types (code, markdown, PDFs, legal text) that need different splitting logic
- Current chunking causes hallucinations because LLM receives incomplete context at chunk boundaries
- Scaling to a large corpus where embedding cost per chunk matters
- Migrating from document-level embedding to chunk-level retrieval

## When NOT To Use

- Documents are short (&lt;500 tokens each) — embed at document level, no chunking needed
- Prototype with &lt;100 documents — use RecursiveCharacterTextSplitter defaults; optimize later
- Cost is the primary constraint and documents are uniform — fixed-size is fastest and cheapest
- Late chunking (Jina embeddings) is available and documents fit in the model's context window — late chunking outperforms all others for contextual coherence

## Content

| File | What's inside |
|------|---------------|
| `content/01-strategies.xml` | Eight strategies with when-to/when-not, parameters, and decision framework |
| `content/02-rules.xml` | Chunk size guidelines, overlap rules, metadata requirements, evaluation metrics, failure modes |

## Templates

| File | Purpose |
|------|---------|
| `templates/chunker-dispatcher.py` | Document-type-aware chunker dispatcher using chonkie |
| `templates/chunking-config.yaml` | YAML config template with all strategy parameters |
