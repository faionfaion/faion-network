---
slug: mlp-planning
tier: pro
group: product
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Minimum Lovable Product planning: a four-layer audit framework (Functional → Reliable → Usable → Delightful) for evolving an MVP that users find "fine" into one they love and recommend.
content_id: "b81d679984db170e"
tags: [mlp, product-polish, retention, delight, mvp-evolution]
---
# MLP Planning

## Summary

**One-sentence:** Minimum Lovable Product planning: a four-layer audit framework (Functional → Reliable → Usable → Delightful) for evolving an MVP that users find "fine" into one they love and recommend.

**One-paragraph:** Minimum Lovable Product planning: a four-layer audit framework (Functional → Reliable → Usable → Delightful) for evolving an MVP that users find "fine" into one they love and recommend. The process identifies delight gaps by clustering feedback where the core job is done but the emotion is missing, then generates a polish backlog ranked by Pain × Frequency × Visibility. MLP threshold: all core features score 4+ on all four layers.

## Applies If (ALL must hold)

- MVP shipped with measurable activation but Day-30 retention plateaus below 25-30%.
- NPS < 30 or churn surveys show users finish the core job but describe the product as "fine" or "okay".
- Retention curve flattens after week 2 — function works, emotion missing.
- About to enter a paid acquisition phase: every dollar spent on a non-lovable product compounds CAC waste.
- Pre-launch in a category where competitors already cleared the "viable" bar.
- Refactor or redesign sprint with explicit budget for polish, copy, micro-interactions.

## Skip If (ANY kills it)

- Pre-MVP — there is nothing to make lovable yet. Use `mvp-scoping` or `minimum-product-frameworks` first.
- Product-market fit not validated — adding delight before demand signal hides the real problem.
- Infrastructure or B2B plumbing where users only interact via API — delight surface is too small.
- Capacity-constrained team mid-incident — Layer 1 and 2 regressions trump delight work.
- Hard-deadline compliance or regulatory features — polish budget is zero until shipped.

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
