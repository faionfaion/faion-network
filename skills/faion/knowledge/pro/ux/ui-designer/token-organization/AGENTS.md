---
slug: token-organization
tier: pro
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A three-layer taxonomy — primitives (raw values) → semantic (purpose-based) → component (exceptions only) — plus a strict naming convention {category}.
content_id: "356f4d04990212e3"
tags: [design-tokens, design-systems, naming-conventions, taxonomy]
---
# Token Organization

## Summary

**One-sentence:** A three-layer taxonomy — primitives (raw values) → semantic (purpose-based) → component (exceptions only) — plus a strict naming convention {category}.

**One-paragraph:** A three-layer taxonomy — primitives (raw values) → semantic (purpose-based) → component (exceptions only) — plus a strict naming convention {category}.{property}.{variant}.{state}. Token names describe purpose, not appearance (color.surface.primary, not blue-500). Keep the set lean: add a new token only when an existing semantic token cannot cover the case; run a duplicate-value detector in CI.

## Applies If (ALL must hold)

- Bootstrapping a new design system's token taxonomy.
- Auditing an existing token set for bloat, naming inconsistency, or aliasing depth.
- Renaming tokens across a large repo without breaking references.
- Reviewing PRs that add new tokens to enforce the lean-first principle.

## Skip If (ANY kills it)

- A 5-token brand palette for a single landing page — overhead exceeds benefit.
- Mid-rebrand with source of truth in flux — stabilize visuals before systematizing.
- Pure component library without theming — indirection adds no payoff.
- Brand-driven marketing assets that change weekly — naming churn kills ROI.

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

- parent skill: `pro/ux/ui-designer/`
