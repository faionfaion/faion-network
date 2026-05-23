---
slug: embedding-chunking-strategies
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Picks chunking strategy (fixed-token, sentence-aware, recursive, semantic, structural) per corpus class plus chunk_size + overlap; benchmarks Recall@10 before deploy.
content_id: "358e2766d2dcfb36"
complexity: medium
produces: code
est_tokens: 3500
tags: [chunking, embeddings, rag, text-splitting, tokenization]
---
# Embedding Chunking Strategies

## Summary

**One-sentence:** Picks chunking strategy (fixed-token, sentence-aware, recursive, semantic, structural) per corpus class plus chunk_size + overlap; benchmarks Recall@10 before deploy.

**One-paragraph:** Wrong chunking is the #1 silent killer of RAG quality. Too small → retriever misses context; too large → retrieval ranks worse and gen blows context. This methodology produces a `ChunkingConfig` artefact and the matching `Chunker` class — strategy picked by corpus class (prose / code / structured), chunk_size tuned by token budget, overlap to bridge across chunks, Recall@10 gate before deploy.

**Ефективно для:**

- New RAG corpus — pick strategy перед embedding.
- Migration зі static splitter → semantic splitter.
- Code corpus — структурний splitter, не token-based.
- Mixed-format corpus (HTML + PDF + Markdown) — per-format strategy.
- Cost-quality tradeoff: smaller chunks = more vectors = better recall at higher cost.

## Applies If (ALL must hold)

- New RAG corpus OR retrieval quality regression vs baseline.
- Domain bench set available (≥50 labeled pairs).
- Token budget allows chunk_size sweep.
- Named owner.

## Skip If (ANY kills it)

- Single-document corpus (chunking optional).
- No bench set → cannot validate.
- Latency budget cannot absorb the sweep.
- Existing chunker validated within last 90 days.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Corpus sample (≥1000 docs) | JSONL | warehouse |
| Domain bench set (50–200 pairs) | JSONL | eval repo |
| Tokenizer (matching embedding model) | tokenizer | platform |
| Embedding model client | client | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[embedding-applications]]` | Pipeline that consumes chunks. |
| `[[rag-bench-harness-template]]` | Bench harness for Recall@10. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules + run/skip terminals | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for chunking-config | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns | ~700 |
| `content/04-procedure.xml` | essential | 5-step: classify → strategy → sweep → bench → deploy | ~700 |
| `content/06-decision-tree.xml` | essential | Routes corpus class to strategy | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-corpus` | sonnet | Per-doc judgment. |
| `sweep-chunk-size` | haiku | Numeric. |
| `recall-gate-review` | opus | Cross-metric synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/chunker.py` | Chunker class with all 5 strategies. |
| `templates/chunking-config.json` | Config skeleton. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-embedding-chunking-strategies.py` | Validate chunking-config | Pre-commit + CI |

## Related

- [[embedding-applications]]
- [[embedding-generation]]
- [[rag-bench-harness-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes corpus class (prose / code / structured / mixed) to strategy default; the bench gate confirms before deploy.
