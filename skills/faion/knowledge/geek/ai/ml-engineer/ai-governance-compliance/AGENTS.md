---
slug: ai-governance-compliance
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Comprehensive framework for AI governance, model risk management, and regulatory compliance in MLOps.
content_id: "2f7186694b8481f5"
tags: [governance, compliance, eu-ai-act, nist-ai-rmf, model-card, fairness, audit-trail, shap, fairlearn, mlflow]
---
# AI Governance and Compliance

## Summary

**One-sentence:** Comprehensive framework for AI governance, model risk management, and regulatory compliance in MLOps.

**One-paragraph:** Comprehensive framework for AI governance, model risk management, and regulatory compliance in MLOps. Provides agent-executable gates, templates, prompts, and verification commands for EU AI Act + NIST AI RMF alignment.

## Applies If (ALL must hold)

- TBD — populate from v1 when-to-use list

## Skip If (ANY kills it)

- Proof-of-concept or internal tool with no production traffic — governance overhead is disproportionate.
- Minimal-risk AI (spam filter, recommender with no legal/financial impact) — no formal governance required by EU AI Act.
- Pre-revenue startup — lightweight logging suffices; formal governance adds friction without regulatory necessity.
- No assigned DRI — governance without ownership degrades into checkbox theater.

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

- parent skill: `geek/ai/ml-engineer/`
