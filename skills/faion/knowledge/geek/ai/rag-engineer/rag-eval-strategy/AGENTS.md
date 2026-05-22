---
slug: rag-eval-strategy
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces an evaluation strategy doc: which metrics, when to run, sampling policy, numeric quality gates.
content_id: "3f280a91a2b13122"
complexity: medium
produces: decision-record
est_tokens: 2800
tags: [rag, evaluation, quality-gates, cost-optimization, strategy]
---
# RAG Evaluation Strategy

## Summary

**One-sentence:** Produces an evaluation strategy doc: which metrics, when to run, sampling policy, numeric quality gates.

**One-paragraph:** RAG evaluation strategy defines which metrics to run, when to run them, how to sample to control LLM-judge costs, and how to set explicit numeric quality gates. The output is a one-page strategy document that anchors all downstream eval pipelines and monitoring configs.

**Ефективно для:** тімлідам, які встановлюють eval-rituals і пороги якості для RAG-продукту.

## Applies If (ALL must hold)

- Before launching a RAG system to production.
- When defining release gates and rollback criteria.
- When cost-per-eval is non-trivial and sampling is required.
- When multiple teams need a shared definition of 'good enough'.

## Skip If (ANY kills it)

- Project is a throwaway prototype with no production target.
- Single-person solo project with no need for shared definition.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Quality targets from product | doc | product |
| Cost budget for evaluations | $/month | finance |
| RAG architecture decision record | md | rag-architecture |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `geek/ai/rag-engineer/rag-eval-retrieval-metrics` | Retrieval metric set. |
| `geek/ai/rag-engineer/rag-eval-generation-metrics` | Generation metric set. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules | ~900 |
| `content/02-output-contract.xml` | essential | JSON schema + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | ~700 |
| `content/06-decision-tree.xml` | essential | Decision tree with rule-id refs | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Draft strategy doc | sonnet | Trade-off framing. |
| Calibrate gates against baselines | haiku | Mechanical aggregation. |

## Templates

| File | Purpose |
|------|---------|
| `templates/eval-strategy.md.tmpl` | Strategy doc skeleton. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rag-eval-strategy.py` | Validates output against the 02-output-contract schema. | Pre-commit; CI. |

## Related

- [[rag-eval-pipeline]]
- [[rag-eval-ab-testing]]
- [[rag-architecture]]

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` decides strategy scope based on production target and team size. Each leaf references a rule id from `01-core-rules.xml`.
