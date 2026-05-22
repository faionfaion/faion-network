---
slug: risk-assessment
tier: pro
group: research
domain: research
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A structured 5-category (market/product/team/financial/operational) risk identification and scoring process using probability x impact matrices.
content_id: "b423b8f400bec9a7"
tags: [risk, risk-register, pre-mortem, due-diligence, startup]
---
# Risk Assessment

## Summary

**One-sentence:** A structured 5-category (market/product/team/financial/operational) risk identification and scoring process using probability x impact matrices.

**One-paragraph:** A structured 5-category (market/product/team/financial/operational) risk identification and scoring process using probability x impact matrices. Each risk gets one owner, one measurable trigger, and a concrete mitigation action (not "monitor + diversify"). Run as a multi-pass agent pipeline: enumerate → red-team pre-mortem → score → human review → convert high-priority risks into SDD tasks.

## Applies If (ALL must hold)

- Pre-launch go/no-go review for a new product, feature, or market entry
- Investor or due-diligence ask requiring a credible risk register plus mitigations
- Quarterly business review where assumptions need re-validation
- After a near-miss incident — formalizing what almost killed the business
- Pivot decision comparing risk profiles of two strategic options
- New regulatory exposure appears on the roadmap (GDPR, AI Act, SOC2, payment rails)

## Skip If (ANY kills it)

- Idea-stage with fewer than 3 customer conversations — risk theater is procrastination
- Tactical sprint planning — use an issue tracker, not a risk register
- One-person side projects with under $1k at stake — overhead exceeds value
- When the team will not assign owners or revisit monthly — a static register is worse than none

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

- parent skill: `pro/research/researcher/`
