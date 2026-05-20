---
slug: token-organization
tier: pro
group: ux
domain: ux-ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A three-tier hierarchy for design tokens — primitives (raw values), semantic tokens (role-based aliases), and component tokens (scoped overrides) — combined with a `{category}.
content_id: "356f4d04990212e3"
tags: [design-tokens, design-systems, naming-convention, hierarchy, theming]
---
# Token Organization: Three-Tier Hierarchy and Naming Convention

## Summary

**One-sentence:** A three-tier hierarchy for design tokens — primitives (raw values), semantic tokens (role-based aliases), and component tokens (scoped overrides) — combined with a `{category}.

**One-paragraph:** A three-tier hierarchy for design tokens — primitives (raw values), semantic tokens (role-based aliases), and component tokens (scoped overrides) — combined with a `{category}.{property}.{variant}.{state}` naming convention that makes tokens self-documenting and prevents bloat.

## Applies If (ALL must hold)

- Bootstrapping a new design system: establishing hierarchy before writing the first token.
- Auditing a sprawling token set (500+ tokens) to collapse aliases, kill duplicates, rename raw-value tokens.
- Onboarding a second platform (mobile after web) where existing names leak platform assumptions.
- Preparing for theming (light/dark/brand) — the semantic layer is mandatory before mode switching.

## Skip If (ANY kills it)

- Single-page marketing site with 8 colors and 3 font sizes — CSS variables in one file suffice.
- Mid-flight design system rewrite when engineers are blocked — global rename without deprecation destroys velocity.
- Without buy-in from at least one designer and one engineer — naming conventions abandoned without authority.

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

- parent skill: `pro/ux/ux-ui-designer/`
