---
slug: eu-ai-act-compliance
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The EU AI Act imposes fines up to EUR 35M or 7% of global turnover for non-compliance.
content_id: "5d4bc55fe9e1f497"
tags: [eu-ai-act, compliance, risk-classification, governance, high-risk]
---
# EU AI Act Compliance

## Summary

**One-sentence:** The EU AI Act imposes fines up to EUR 35M or 7% of global turnover for non-compliance.

**One-paragraph:** The EU AI Act imposes fines up to EUR 35M or 7% of global turnover for non-compliance. Risk classification determines which articles apply; incorrect classification — either under- or over-scoping — leads to either regulatory exposure or unnecessary engineering cost. Agents producing compliance drafts must cite specific articles and flag ambiguous cases for legal review.

## Applies If (ALL must hold)

- Building or deploying an AI system targeting EU users after August 2024
- Any system processing biometrics, employment decisions, credit scoring, education admissions, or critical infrastructure — all are Annex III high-risk
- Deploying a GPAI model (General Purpose AI) with >10^25 FLOPs training compute (systemic risk tier, Aug 2025 deadline)
- Integrating third-party LLM APIs where the provider's compliance does not cover downstream deployer obligations
- Conducting a pre-launch compliance gap analysis

## Skip If (ANY kills it)

- Products deployed exclusively outside the EU with no EU users or EU-based processing
- Purely internal tools with no impact on individuals' rights or safety (minimal risk tier — no obligations)
- R&D activities exempt under Article 2(6) — lab testing does not require compliance
- Open-source models released without commercial intent may have reduced obligations (verify per Article 2(12))

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
