---
slug: ai-enhanced-design-systems
tier: geek
group: ux
domain: ux-ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: AI tooling for scaling design systems with a solid token foundation: automated documentation generation from component source, token violation scanning, Figma-to-code diff, and variant generation.
content_id: "bd294b563bb9fdc2"
tags: [design-systems, automation, documentation, tokens, component-library]
---
# AI-Enhanced Design Systems

## Summary

**One-sentence:** AI tooling for scaling design systems with a solid token foundation: automated documentation generation from component source, token violation scanning, Figma-to-code diff, and variant generation.

**One-paragraph:** AI tooling for scaling design systems with a solid token foundation: automated documentation generation from component source, token violation scanning, Figma-to-code diff, and variant generation. AI amplifies what exists — it will not fix an inconsistent or poorly structured system.

## Applies If (ALL must hold)

- Design system has a solid token foundation and needs to scale component variants
- Documentation perpetually lags implementation — agent auto-generates from component source
- Design-to-code gap causes inconsistency — agent reconciles Figma tokens vs. CSS/Tailwind variables
- Team growing and consistency enforcement needs automation beyond manual design review
- Component adoption metrics are missing

## Skip If (ANY kills it)

- Weak or inconsistent design system foundation — AI amplifies existing problems
- No structured token system exists — generated variations will be arbitrary
- Component naming is inconsistent across Figma and codebase — AI propagates inconsistency at scale
- Fewer than ~30 components — automation overhead exceeds manual maintenance cost
- No agreed single source of truth (Figma vs. code tokens)

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

- parent skill: `geek/ux/ux-ui-designer/`
