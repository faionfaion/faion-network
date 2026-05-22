---
slug: embeddings-production-ops
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Production embeddings operations: latency SLO, rate-limit handling, cost tracking, fault tolerance, model migration playbook.
content_id: "0532c5515c1bdfd6"
complexity: deep
produces: config
est_tokens: 4200
tags: [embeddings, production, monitoring, debugging, cost-optimization]
---
# Embeddings Production Ops

## Summary

**One-sentence:** Production embeddings operations: latency SLO, rate-limit handling, cost tracking, fault tolerance, model migration playbook.

**One-paragraph:** Running embedding systems in production beyond «it works in dev» requires latency SLOs, exponential-backoff rate-limit handling, per-tenant cost accounting, fault tolerance for provider outages, and a model-migration playbook (reindex without downtime). This methodology produces an `embeddings-ops.yaml` config + a runbook covering the five operational gates.

**Ефективно для:** ML eng, що вже зловили 429 / outage / cost-spike і хочуть закрити цикл за один artefact.

## Applies If (ALL must hold)

- embeddings power production retrieval
- monthly query volume > 100k
- you have an SLO (latency_p95, success_rate) defined
- cost tracking is required (per tenant or per use case)
- provider outage has happened or is plausible

## Skip If (ANY kills it)

- prototype or internal-only — gates are overkill
- single-tenant + low volume
- embedding is computed offline only — no real-time ops
- you use a fully-managed search-as-a-service — vendor handles ops

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Use-case brief | text | Author / owner |
| Tier-manifest entry | JSON | `skills/tier-manifest.json` |
| Eval / fixture data (when applicable) | jsonl | Repo `tests/fixtures/` |
| Named approver | role:person | Org RACI |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/llm-integration/semantic-xml-content` | Authoring shape for `content/*.xml`. |
| `geek/ai/ml-engineer/ai-agent-patterns` | Pattern catalogue for agent loops referenced from this methodology. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with statement + rationale + source | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for produces=config + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | ~900 |
| `content/04-procedure.xml` | medium | 5-step procedure with input / action / output / decision-gate | ~700 |
| `content/05-examples.xml` | medium | End-to-end worked example | ~500 |
| `content/06-decision-tree.xml` | essential | Root question + branches with `when` observables → conclusion(ref=rule-id) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `plan-step` | sonnet | Standard reasoning over the procedure / scoring axes. |
| `author-output` | sonnet | Produces the artefact in the shape `produces=config`. |
| `audit-validate` | haiku | Mechanical schema check via `scripts/validate-embeddings-production-ops.py`. |
| `senior-review` | opus | Cross-artefact judgement on rejection / approval. |

## Templates

| File | Purpose |
|------|---------|
| `templates/embeddings-ops.yaml` | Production ops config skeleton |
| `templates/rate-limit-handler.py` | Exponential-backoff + jitter wrapper |
| `templates/cost-attribution.py` | Per-call (tenant, use case, tokens, $) logger |
| `templates/migration-playbook.md` | Dual-index migration runbook |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-embeddings-production-ops.py` | Validate an output artefact against the JSON schema from `content/02-output-contract.xml`. | Pre-merge on the artefact PR + `--self-test` in CI. |

## Related

- [[ai-agent-patterns]] — pattern catalogue this methodology routes through.
- [[agents-production-deployment]] — production gates this methodology feeds into.
- external: rule rationales cite the sources in `content/01-core-rules.xml`.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` picks the right rule branch for the current task. Branches use observable inputs (numeric / boolean / categorical) and every leaf cites one of `r1-slo-defined`, `r2-rate-limit-handling`, `r3-cost-attribution`, `r4-fault-tolerance`, `r5-migration-playbook` from `content/01-core-rules.xml`.
