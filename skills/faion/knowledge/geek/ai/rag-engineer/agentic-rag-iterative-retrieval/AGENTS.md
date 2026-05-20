---
slug: agentic-rag-iterative-retrieval
tier: geek
group: ai
domain: rag-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Traditional RAG performs a single retrieval pass with a fixed pipeline.
content_id: "4bf6dec87d824bf8"
tags: [rag, agentic, retrieval, multi-hop, llm]
---
# Agentic RAG — Iterative Retrieval

## Summary

**One-sentence:** Traditional RAG performs a single retrieval pass with a fixed pipeline.

**One-paragraph:** Traditional RAG performs a single retrieval pass with a fixed pipeline. Iterative retrieval lets an LLM decide whether the retrieved context is sufficient, and if not, generates a refined query and retrieves again — up to a configurable maximum iteration count.

## Applies If (ALL must hold)

- Questions require combining information from multiple disjoint documents (multi-hop QA).
- A single retrieval pass consistently returns insufficient or partially relevant context.
- Research synthesis tasks: explore → evaluate → refine → conclude.
- Latency SLA allows 3–10s per query and cost budget accepts 3–5x single-pass RAG.

## Skip If (ANY kills it)

- Single-turn factual lookup where standard RAG suffices — agentic loop adds 3–5x latency and cost.
- Latency-critical user-facing queries (under 2s SLA) — iterative retrieval typically takes 3–10s.
- Well-structured corpora with high coverage where iterative gains are marginal.
- Untrusted or adversarial input corpora — iterative loops can be exploited via prompt injection in documents.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/ai/rag-engineer/`
