---
slug: rag-eval-ab-testing
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Runs an interleaved A/B test of two RAG configurations on a shared question set and reports per-config metrics with a promote/reject recommendation.
content_id: "ec005996c19dff9a"
complexity: medium
produces: report
est_tokens: 3000
tags: [rag, ab-testing, evaluation, configuration]
---
# RAG A/B Testing Framework

## Summary

**One-sentence:** Runs an interleaved A/B test of two RAG configurations on a shared question set and reports per-config metrics with a promote/reject recommendation.

**One-paragraph:** A/B testing for RAG configurations runs the same question set through two pipeline variants and compares their results. The baseline framework measures latency and source count; a full quality comparison requires integrating the RAGAS evaluation loop per configuration. Use A/B testing to validate parameter changes (chunk size, embedding model, top-K, reranker) before promoting config B to production.

**Ефективно для:** команд, які хочуть перевірити config-зміну (chunk size, embedding model, reranker) до промоушн в production.

## Applies If (ALL must hold)

- Comparing different chunk sizes for the same corpus.
- Evaluating the impact of adding or swapping a reranker model.
- Comparing embedding models (e.g., text-embedding-3-large vs voyage-3).
- Validating any config parameter change before promoting it to production.

## Skip If (ANY kills it)

- Test set has &lt;20 questions — differences are within statistical noise.
- The two configurations are not isolated (share index state or caches).
- Only latency matters and quality is irrelevant — just benchmark directly.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Config A | YAML | current prod |
| Config B | YAML | candidate |
| Shared test set | JSONL {query, ground_truth} | rag-eval-test-set-generation |
| RAGAS judge | LLM credentials | env |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `geek/ai/rag-engineer/rag-eval-pipeline` | Provides the per-config eval runner. |
| `geek/ai/rag-engineer/rag-eval-strategy` | Defines numeric quality gates. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: interleave A/B, isolate state, ≥20 questions, paired stats, quality &gt; latency | ~800 |
| `content/02-output-contract.xml` | essential | JSON schema for AB report | ~700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: non-interleaved batches, latency-only signal, leak via shared cache | ~700 |
| `content/04-procedure.xml` | medium | 5-step procedure | ~700 |
| `content/06-decision-tree.xml` | essential | Tree for promote/reject/run-more | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Run interleaved trials | haiku | Mechanical. |
| Compute paired metrics | haiku | Pure arithmetic. |
| Write promotion recommendation | sonnet | Trade-off framing. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ab-runner.py.tmpl` | Interleaved runner that fires A and B per question. |
| `templates/ab-report.md.tmpl` | Report skeleton with per-config metrics and recommendation. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rag-eval-ab-testing.py` | Validates AB report JSON. | Pre-commit; CI. |

## Related

- [[rag-eval-pipeline]]
- [[rag-eval-strategy]]
- [[rag-eval-test-set-generation]]

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` decides promotion: root question — "Is the per-question paired difference between A and B statistically significant (p&lt;0.05)?". Branches lead to promote-B, keep-A, or "run more trials". Each leaf references a rule.
