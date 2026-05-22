---
slug: technical-debt-management
tier: solo
group: product
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Systematic process for making technical debt visible, quantifying its interest cost, prioritizing paydown against the roadmap, and allocating 15-20% of sprint capacity continuously.
content_id: "b187463217f158b6"
tags: [technical-debt, refactoring, code-quality, sprint-planning, engineering-velocity]
---
# Technical Debt Management

## Summary

**One-sentence:** Systematic process for making technical debt visible, quantifying its interest cost, prioritizing paydown against the roadmap, and allocating 15-20% of sprint capacity continuously.

**One-paragraph:** Systematic process for making technical debt visible, quantifying its interest cost, prioritizing paydown against the roadmap, and allocating 15-20% of sprint capacity continuously. Classifies debt into 6 types (deliberate, accidental, bit-rot, design, documentation, test), scores each on Interest/Contagion/Effort/Alignment, and sequences paydown aligned with planned feature work to minimize marginal cost.

## Applies If (ALL must hold)

- Codebase has aging dependencies, fragmented patterns, and "fear zones" engineers avoid.
- Onboarding: agent surveys repo for hot-spots and surfaces undocumented assumptions.
- Quarterly debt-paydown planning: scoring and sequencing the register against upcoming roadmap.
- Pre-acquisition or pre-investment due diligence: producing defensible debt inventory.
- Migration planning (lib upgrade, framework jump, monolith decomposition).

## Skip If (ANY kills it)

- One-person codebase under 6 months old — debt is rounding error, ship features.
- Debt that is actually a missing feature — do not classify "we never built X" as "we built X badly".
- Production incident response — debt management is a planning activity, not firefighting.
- Code-quality theater — do not run an agent to generate a debt list nobody will fund.

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

- parent skill: `solo/product/product-operations/`
