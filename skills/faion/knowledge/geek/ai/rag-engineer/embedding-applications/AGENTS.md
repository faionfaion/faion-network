---
slug: embedding-applications
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: End-to-end embedding pipeline — MTEB-anchored model selection plus domain benchmarking, batched insertion, normalized cosine, model-version metadata, Recall@10 quality gate.
content_id: "0e2203ee9405c78b"
complexity: deep
produces: code
est_tokens: 4000
tags: [embeddings, benchmarking, vector-databases, rag, indexing]
---
# Embedding Applications

## Summary

**One-sentence:** End-to-end embedding pipeline — MTEB-anchored model selection plus domain benchmarking, batched insertion, normalized cosine, model-version metadata, Recall@10 quality gate.

**One-paragraph:** Pick the wrong embedding model and the whole RAG underperforms; pick right but skip normalization or batching and cost/latency explode. This methodology produces a multi-agent embedding pipeline: model selection (MTEB retrieval score + 50–200 domain pairs), embedding generation (batched + backoff), vector DB insertion (normalized + version metadata), and a Recall@10 quality gate that blocks promotion to production.

**Ефективно для:**

- New RAG project обирати embedding model — MTEB ≠ retrieval rank.
- Domain-specific corpus (legal, biomedical, code) — custom bench mandatory.
- Cross-provider migration (OpenAI ↔ Cohere ↔ Voyage ↔ local).
- Re-indexing trigger при model deprecation.
- Cost/quality trade-off через Matryoshka dims.

## Applies If (ALL must hold)

- New RAG pipeline OR model migration.
- 50–200 labeled domain query/doc pairs available.
- Vector DB with cosine support.
- Named owner.

## Skip If (ANY kills it)

- General-purpose corpus already well-served by ada-002 baseline.
- &lt;50 labeled domain pairs (cannot bench reliably).
- Single-model lock-in for legal reasons.
- No re-indexing budget.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Domain corpus sample | JSONL | warehouse |
| Labeled query/doc pairs (50–200) | JSONL | eval repo |
| Candidate model catalog | YAML | platform |
| Vector DB client (Qdrant/pgvector/Weaviate) | client | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[embedding-models]]` | Provider-specific rules. |
| `[[embedding-generation]]` | Batching + normalization rules. |
| `[[rag-bench-harness-template]]` | Bench harness. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules + run/skip terminals | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for embedding-pipeline-config | ~700 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns with detector + repair | ~800 |
| `content/04-procedure.xml` | essential | 5-step: shortlist → domain-bench → wire batched → quality-gate → deploy | ~800 |
| `content/06-decision-tree.xml` | essential | Routes domain to model class | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `shortlist-models` | sonnet | MTEB filter + domain knowledge. |
| `run-domain-bench` | haiku | Mechanical metric compute. |
| `quality-gate-review` | opus | Cross-metric synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/embedding_pipeline.py` | Pipeline class with model selection + bench + insert + gate. |
| `templates/embedding-pipeline-config.json` | Config skeleton. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-embedding-applications.py` | Validate embedding-pipeline-config | Pre-commit + CI |

## Related

- [[embedding-models]]
- [[embedding-generation]]
- [[embedding-cost-optimization]]
- [[rag-bench-harness-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes domain class to candidate model set (general / code / multilingual / legal-biomedical) and gates promotion on Recall@10 threshold.
