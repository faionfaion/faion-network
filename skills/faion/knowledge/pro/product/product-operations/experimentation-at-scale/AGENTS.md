---
slug: experimentation-at-scale
tier: pro
group: product
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Enterprise experimentation is a disciplined platform — not ad-hoc A/B testing — with defined hypothesis intake, pre-registered metrics, guardrails, SRM checks, and a learning-extraction step.
content_id: "4e204465f81afa3d"
tags: [a-b-testing, experimentation, statistics, agent-ops, feature-flags]
---
# Experimentation at Scale

## Summary

**One-sentence:** Enterprise experimentation is a disciplined platform — not ad-hoc A/B testing — with defined hypothesis intake, pre-registered metrics, guardrails, SRM checks, and a learning-extraction step.

**One-paragraph:** Enterprise experimentation is a disciplined platform — not ad-hoc A/B testing — with defined hypothesis intake, pre-registered metrics, guardrails, SRM checks, and a learning-extraction step. Maturity runs from Level 1 (ad-hoc, no standards) to Level 4 (every decision backed by an experiment). The full agentic loop covers: hypothesis authoring → sample-size math → flag deployment → hourly SRM watch → daily metric watch → readout → cross-cutting learnings memo.

## Applies If (ALL must hold)

- Product orgs running 50+ live A/B tests per quarter where coordination has outgrown spreadsheets
- Maturity-level transitions: when formalizing hypothesis intake, sample-size math, and guardrails
- Feature-flag rollouts tied to experiment readouts requiring automated SRM checks
- Warehouse-native shops (Snowflake/BigQuery) driving Eppo/Statsig from dbt models
- Solopreneur / small team needing an agent to generate hypotheses, monitor results, and emit readouts
- Post-launch "what did we learn?" synthesis across an experiment registry

## Skip If (ANY kills it)

- Pre-PMF with <1k weekly active users — sample-size math demands months per test; use qualitative discovery instead
- Single-shot launches where a holdout is impossible or unethical
- High-stakes irreversible decisions (pricing rebrand, contract terms, safety-critical UX) — use multi-method evidence, not a single A/B
- Enterprise B2B with <50 accounts — sample size makes A/B impractical; use cohort analysis
- Teams without a metrics governance owner (single source of truth for metric definitions)
- Compliance-bound surfaces (HIPAA, payment flows, KYC) where variants must clear legal before ship

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

- parent skill: `pro/product/product-operations/`
