---
slug: minimum-product-frameworks
tier: solo
group: product
domain: product-planning
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A decision matrix for choosing the right "minimum X product" framework for a given market context.
content_id: "dc964a3963bcc535"
tags: [mvp, frameworks, product-scoping, market-fit, release-strategy]
---
# Minimum Product Frameworks

## Summary

**One-sentence:** A decision matrix for choosing the right "minimum X product" framework for a given market context.

**One-paragraph:** A decision matrix for choosing the right "minimum X product" framework for a given market context. Nine frameworks — MVP, MLP, MMP, MAC, RAT, MDP, MVA, MFP, SLC — each suited to a different combination of market uncertainty, competitive density, and buyer type. The core rule: picking the wrong framework wastes validation budget and may guarantee failure in crowded markets where users already have "good enough" alternatives.

## Applies If (ALL must hold)

- Trigger: starting a new product and deciding how much to build before first release.
- Trigger: switching market context (e.g. moving from B2C to B2B) and re-scoping.
- Trigger: team debate "is this MVP or MLP?" — use the decision matrix to resolve.
- Trigger: competitive analysis reveals incumbent products are already polished.
- Trigger: spec.md / SDD feature kickoff before writing implementation-plan.md.
- Trigger: pivot decision — last release missed adoption KPI; re-scope with a different framework.

## Skip If (ANY kills it)

- Framework already chosen and validated — don't re-litigate mid-build.
- Pure technical feasibility spikes — use MFP by default, no matrix needed.
- Internal tooling with a captive user base — minimal standards differ.
- Bug-fix or maintenance release — framework choice does not apply.

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

- parent skill: `solo/product/product-planning/`
