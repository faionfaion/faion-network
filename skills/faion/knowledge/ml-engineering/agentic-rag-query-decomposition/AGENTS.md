# Agentic RAG — Query Decomposition

## Summary

**One-sentence:** Decomposes complex queries into 2–4 atomic sub-queries, retrieves in parallel, tracks coverage; falls back to single-pass when decomposition collapses to 1 sub-query.

**One-paragraph:** Complex queries with multiple intents waste retrieval budget when run as a single embedding. This methodology produces a `QueryDecomposer` class: a planning LLM emits 2–4 atomic sub-queries; each is retrieved in parallel via asyncio.gather; results merged with coverage tracking. If decomposition returns &lt;2 sub-queries, the original is treated atomic. If &gt;4, only the top-4 by confidence kept. Coverage gaps surfaced for review.

**Ефективно для:**

- Complex compound queries з ≥2 distinct intents.
- Latency budget allows parallel sub-query fanout.
- Track coverage gaps (sub-query without high-confidence chunk).
- Sub-query cache within one agentic run.
- Bridge from `[[agentic-rag-iterative-retrieval]]` for compound questions.

## Applies If (ALL must hold)

- Question class includes multi-intent compound queries.
- Parallel retrieval supported by infra.
- Planning LLM available distinct from generator.
- Coverage-gap surfacing acceptable (vs silent drops).

## Skip If (ANY kills it)

- Single-intent atomic queries — decomposition adds no value.
- Sequential-only retriever (no parallel infra).
- Cost budget cannot absorb planning + N retrieval rounds.
- No coverage-gap consumer (gaps would be ignored).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Planning model client | provider client | platform |
| Retriever runner | python | service repo |
| Parallel executor (asyncio / pool) | runtime | platform |
| Confidence threshold | float | retrieval policy |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[agentic-rag-iterative-retrieval]]` | Iterative loop methodology. |
| `[[embedding-generation]]` | Shared embedder. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 3 rules + run/skip terminals | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for decomposer-config | ~700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with detector + repair | ~700 |
| `content/04-procedure.xml` | essential | 5-step: plan → cap → parallel retrieve → coverage → merge | ~700 |
| `content/06-decision-tree.xml` | essential | Routes question class to decomposition vs atomic | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `plan-sub-queries` | sonnet | Planning judgment. |
| `score-sub-query-confidence` | haiku | Numeric scoring. |
| `merge-context` | sonnet | Multi-result synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/query_decomposer.py` | QueryDecomposer class with parallel fanout + coverage. |
| `templates/decomposer-config.json` | Config skeleton. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agentic-rag-query-decomposition.py` | Validate decomposer-config | Pre-commit + CI |

## Related

- [[agentic-rag-iterative-retrieval]]
- [[agentic-rag-self-correction]]
- [[rag-bench-harness-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes to decomposition when question class is compound + parallel retrieval available. Atomic queries fall back to single-pass.
