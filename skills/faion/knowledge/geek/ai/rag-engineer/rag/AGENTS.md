---
slug: rag
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Builds an end-to-end RAG pipeline (ingest → retrieve → rerank → generate) with cited answers and a launch-gate at MRR>0.7 and faithfulness>0.9.
content_id: "3328b6fffebf5dd2"
complexity: deep
produces: code
est_tokens: 5000
tags: [rag, retrieval, generation, vector-search, llm]
---
# RAG Pipeline

## Summary

**One-sentence:** Builds an end-to-end RAG pipeline (ingest → retrieve → rerank → generate) with cited answers and a launch-gate at MRR&gt;0.7 and faithfulness&gt;0.9.

**One-paragraph:** A Retrieval-Augmented Generation pipeline ingests documents (load → chunk → embed → store), retrieves relevant chunks for a query (embed → vector search → rerank), and generates a grounded answer with source citations. Key invariants: chunk quality bounds retrieval quality; hybrid search is the default; reranking is required for production accuracy; evaluate with MRR&gt;0.7 and faithfulness&gt;0.9 before launch.

**Ефективно для:** команд, які будують AI-помічника на приватному/часто-оновлюваному корпусі і потребують грунтованих відповідей із цитатами.

## Applies If (ALL must hold)

- Agent must answer questions grounded in a private or frequently-updated corpus.
- Hallucination on domain-specific topics is unacceptable.
- Knowledge assistant over PDFs / docs / wikis / code.
- Citation / source attribution is required for compliance or user trust.

## Skip If (ANY kills it)

- Document set is tiny (&lt;50 chunks) and fits in context — stuff the full context instead.
- Questions are purely general knowledge — RAG adds latency with no accuracy gain.
- Data is real-time (stock prices, live APIs) — use live tool calls.
- Latency budget &lt; 200ms — embed + retrieve overhead exceeds SLA.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Document corpus | PDF / md / txt / html | ingestion job |
| Vector DB credentials | env | infra |
| Embedding model | provider | embedding-models |
| Reranker | cross-encoder or API | reranking-models |
| Eval test set | JSONL {query, expected_ids} | rag-eval-test-set-generation |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `geek/ai/rag-engineer/rag-architecture` | Architecture decisions feed this build. |
| `geek/ai/rag-engineer/chunking-basics` | Chunking quality bounds retrieval. |
| `geek/ai/rag-engineer/vector-database-setup` | Backend choice. |
| `geek/ai/rag-engineer/reranking-two-stage` | Production reranker. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: chunk + metadata, hybrid default, rerank top-20→5, context order, answer-only-from-context, MRR/faithfulness gate | ~1100 |
| `content/02-output-contract.xml` | essential | JSON schema for one RAG answer (text + citations[] + faithfulness + metrics) | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: lost-in-the-middle, hallucinated citations, no eval gate, post-index metadata add | ~800 |
| `content/04-procedure.xml` | medium | 6-step build procedure | ~900 |
| `content/06-decision-tree.xml` | essential | Tree picking RAG vs context-stuffing vs agentic-RAG | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Chunk + embed corpus | haiku | Mechanical batch. |
| Generate cited answer | sonnet | Quality grounding. |
| Faithfulness scoring | sonnet | Judge-style eval. |
| Architecture decisions | opus | Trade-offs. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rag-pipeline.py.tmpl` | End-to-end skeleton: ingest, retrieve, rerank, generate. |
| `templates/answer-prompt.txt` | "Answer ONLY from the provided context" system prompt with citation format. |
| `templates/_smoke-test.py` | Minimal end-to-end smoke test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rag.py` | Validates a RAG answer against schema. | Pre-commit; CI. |

## Related

- [[rag-architecture]]
- [[rag-implementation]]
- [[rag-eval-strategy]]
- [[reranking-two-stage]]

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` picks the right approach: root question — "Does the corpus fit a single context window AND token-cost is acceptable?". Branches lead to context-stuffing (small corpus), standard RAG (default), or agentic-RAG (multi-hop questions). Each leaf references a core rule.
