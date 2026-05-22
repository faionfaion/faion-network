---
slug: minimum-product-frameworks
tier: pro
group: product
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A selection matrix for choosing one of nine "minimum product" frameworks — MVP, MLP, MMP, MAC, RAT, MDP, MVA, MFP, SLC — before the first spec.
content_id: "dc964a3963bcc535"
tags: [minimum-product, framework-selection, product-strategy, mvp, market-strategy]
---
# Minimum Product Frameworks

## Summary

**One-sentence:** A selection matrix for choosing one of nine "minimum product" frameworks — MVP, MLP, MMP, MAC, RAT, MDP, MVA, MFP, SLC — before the first spec.

**One-paragraph:** A selection matrix for choosing one of nine "minimum product" frameworks — MVP, MLP, MMP, MAC, RAT, MDP, MVA, MFP, SLC — before the first spec.md is written. The matrix maps market condition (blue/red ocean), buyer type (B2B/consumer), differentiator, and technical uncertainty to the right framework. Each choice must be versioned in a framework-choice.md with two explicit exit criteria before scoping begins.

## Applies If (ALL must hold)

- New product or major module — before the first spec.md exists.
- Team is reflexively saying "let's ship an MVP" without checking market density, buyer type, or differentiator.
- Pivot moment: current build is failing on retention or conversion — re-pick the framework before re-scoping.
- Multiple stakeholders disagree on what "minimum" means — use the matrix as a forcing function.
- Pre-investment or pre-board memo: justify the chosen framework against blue/red ocean and ICP positioning.

## Skip If (ANY kills it)

- Methodology already chosen and validated — go straight to that framework's scoping doc; do not re-litigate.
- Pure feature work inside a shipped product — use release-planning, feature-prioritization-rice, or MoSCoW instead.
- Hard-deadline regulated launches where scope is dictated by compliance, not strategy.
- Tiny fix-it-fast tasks (<1 sprint) — framework choice overhead exceeds value.
- Internal tools with one stakeholder — pick MFP and move on.

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

- parent skill: `pro/product/product-manager/`
