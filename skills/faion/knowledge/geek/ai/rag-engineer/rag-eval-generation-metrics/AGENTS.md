---
slug: rag-eval-generation-metrics
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Generation metrics measure whether the RAG pipeline produces answers that are faithful to the retrieved context, relevant to the question, and sourced from contextually relevant documents.
content_id: "3db33b525ff22ca9"
tags: [rag, evaluation, generation, faithfulness, ragas]
---
# RAG Generation Quality Metrics

## Summary

**One-sentence:** Generation metrics measure whether the RAG pipeline produces answers that are faithful to the retrieved context, relevant to the question, and sourced from contextually relevant documents.

**One-paragraph:** Generation metrics measure whether the RAG pipeline produces answers that are faithful to the retrieved context, relevant to the question, and sourced from contextually relevant documents. The three core metrics — Faithfulness, Answer Relevance, and Context Relevance — form the RAG Triad and are computed via LLM-judge prompts or the RAGAS framework.

## Applies If (ALL must hold)

- Evaluating whether generated answers hallucinate (Faithfulness) — essential before any production deployment.
- Checking whether answers address the user question (Answer Relevance) — catches verbosity, off-topic responses, or incomplete answers.
- Checking whether retrieved context contains the information needed to answer (Context Relevance) — diagnoses retrieval problems at the semantic level, beyond what Precision@K captures.
- Running the RAGAS framework for a full RAG Triad score in development and pre-production.
- Sampling 10-20% of production queries for offline faithfulness monitoring.

## Skip If (ANY kills it)

- Real-time per-query scoring in production — LLM-judge metrics (faithfulness, relevance) are too slow and expensive at query time; use offline sampling on a subset instead.
- Cross-LLM comparisons of metric scores — RAGAS metrics use OpenAI by default; swapping to a different LLM evaluator changes metric values significantly and results are not cross-LLM-comparable.
- Replacing retrieval metrics — low faithfulness with high Precision@K points to a generation problem; without retrieval metrics you cannot distinguish the two failure modes.

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
