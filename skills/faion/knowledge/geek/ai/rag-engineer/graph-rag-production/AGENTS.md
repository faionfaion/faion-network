---
slug: graph-rag-production
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Production-ready GraphRAG deployment: query routing (GLOBAL/LOCAL/COMMUNITY), caching layer, incremental updates, observability, and cost guardrails.
content_id: "b511f9b80d776584"
complexity: deep
produces: config
est_tokens: 4300
tags: [graph-rag, production, deployment, observability, cost-control]
---
# Graph RAG in Production

## Summary

**One-sentence:** Production-ready GraphRAG deployment: query routing (GLOBAL/LOCAL/COMMUNITY), caching layer, incremental updates, observability, and cost guardrails.

**One-paragraph:** Production-ready GraphRAG deployment: query routing (GLOBAL/LOCAL/COMMUNITY), caching layer, incremental updates, observability, and cost guardrails. The methodology is testable end-to-end: each artefact it produces conforms to the JSON Schema in `content/02-output-contract.xml`, every claim in the body resolves to a rule in `content/01-core-rules.xml`, and the decision-tree in `content/06-decision-tree.xml` routes observable inputs to the right rule.

**Ефективно для:**

- Виходиш з POC у production: query routing + cache + cost caps.
- Inкрементальні оновлення графа без full re-index (delta ingestion).
- Observability: per-query type latency, cost, hit-rate by community.
- Cost guardrails: $/1k queries cap + circuit breaker на community summarization.

## Applies If (ALL must hold)

- GraphRAG index уже побудовано (див. graph-rag-indexing).
- Production traffic ≥ 1k queries/day з SLO < 5s p95.
- Бюджетні обмеження вимагають per-query cost tracking.

## Skip If (ANY kills it)

- POC або демо без SLO — production-патерни overkill.
- Read-only static index без оновлень — incremental gear не потрібен.
- < 100 queries/day — cache + routing payoff нульовий.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| graphrag index | directory with chunks/entities/graph/summaries | graph-rag-indexing output |
| traffic profile | JSON {qps, query_types[]} | product metrics |
| cost budget | USD/day cap | finance |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[graph-rag-indexing]] | index manifest committed and versioned |
| [[graph-rag-retrieval]] | retrieval contract finalized |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom/root-cause/fix) | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure (input/action/output/decision-gate) | 900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule in 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| classify-input | sonnet | Light judgment; identifies branch in decision tree. |
| draft-output | sonnet | Drafting the output artefact per schema. |
| validate-output | haiku | Mechanical schema validation via script. |

## Templates

| File | Purpose |
|------|---------|
| `templates/graphrag-production.yaml` | Service config matching schema |
| `templates/router.py` | Ingress query router scaffold |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-graph-rag-production.py` | Validate output artefact against schema in 02-output-contract.xml | CI on each artefact change; pre-commit |

## Related

- [[graph-rag-indexing]]
- [[graph-rag-retrieval]]
- [[rag-eval-production-monitoring]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from the question "Is the GraphRAG service handling live production traffic with SLO + cost constraints?" and routes observable input signals to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Apply it whenever the input shape changes or before scaling a pilot run.
