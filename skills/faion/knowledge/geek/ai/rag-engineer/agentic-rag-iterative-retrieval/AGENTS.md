---
slug: agentic-rag-iterative-retrieval
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces an iterative-retrieval RAG agent class — LLM judge decides sufficiency, refines query, retries up to a hard cap; drift detection + dedup + per-step model routing.
content_id: "4bf6dec87d824bf8"
complexity: deep
produces: code
est_tokens: 3800
tags: [rag, agentic, iterative-retrieval, multi-hop, llm-judge]
---
# Agentic RAG — Iterative Retrieval

## Summary

**One-sentence:** Produces an iterative-retrieval RAG agent class — LLM judge decides sufficiency, refines query, retries up to a hard cap; drift detection + dedup + per-step model routing.

**One-paragraph:** Single-pass RAG fails on multi-hop questions where the answer lives across disjoint chunks. This methodology produces an `IterativeRetriever` class that runs retrieve → judge sufficiency → refine query → retrieve loop up to `max_iterations` (default 3, hard cap 5). Sufficiency judge runs on cheap model (Haiku/Sonnet); final answer synthesis on Opus. Drift detection: cosine sim between original and refined query embeddings <0.7 → reset to original. Dedup by chunk_id between iterations.

**Ефективно для:**

- Multi-hop QA — answer require combining ≥2 disjoint docs.
- Research synthesis tasks: explore → evaluate → refine → conclude.
- Latency budget 3–10s per query and cost budget 3–5x baseline RAG.
- Adversarial-corpus-aware deployments — judge model must differ from generator.
- Bounded budget — hard iteration cap is non-negotiable.

## Applies If (ALL must hold)

- Multi-hop / synthesis questions where single-pass RAG fails &gt;20% of evals.
- Latency SLA ≥3s allowed.
- Cost budget supports 3–5x single-pass RAG.
- Sufficiency judge model available distinct from generator.

## Skip If (ANY kills it)

- Single-turn factual lookup — standard RAG suffices.
- &lt;2s latency SLA.
- Untrusted/adversarial corpora без sanitisation pipeline.
- Cost budget cannot absorb 3–5x.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Query embedder | model name + dim | platform |
| Retriever (BM25 / dense / hybrid) | runner | service repo |
| Judge model client | provider client | platform |
| Generator model client | provider client | platform |
| Chunk-id dedup helper | python | service repo |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[embedding-generation]]` | Same-model indexing/query rule applies. |
| `[[rag-bench-harness-template]]` | Bench harness consumes the agent. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4 rules + run/skip terminals | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for iterative-retriever-config | ~700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with detector + repair | ~700 |
| `content/04-procedure.xml` | essential | 5-step: wire retriever → wire judge → loop + dedup → drift gate → generator | ~700 |
| `content/06-decision-tree.xml` | essential | Routes question class to iterative vs single-pass | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `sufficiency-judge` | haiku | Yes/no judgement; cheap. |
| `query-refinement` | sonnet | Light judgment. |
| `final-answer-synthesis` | opus | Multi-chunk reasoning. |

## Templates

| File | Purpose |
|------|---------|
| `templates/iterative_retriever.py` | IterativeRetriever class with budget + dedup + drift gate. |
| `templates/iterative-retriever-config.json` | Config skeleton. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agentic-rag-iterative-retrieval.py` | Validate iterative-retriever-config | Pre-commit + CI |

## Related

- [[agentic-rag-query-decomposition]]
- [[agentic-rag-self-correction]]
- [[rag-bench-harness-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes to iterative retrieval only for multi-hop / synthesis questions with latency tolerance ≥3s. Walk it before wiring; using iterative for single-hop wastes 3–5x latency.
