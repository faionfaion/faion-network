---
slug: consistency-standards
tier: solo
group: ux
domain: ux-ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Nielsen Heuristic #4: users should not wonder whether different words, situations, or actions mean the same thing.
content_id: "053ef7e57ea7ee24"
tags: [consistency, design-systems, usability-heuristics, design-audit, ui-standards]
---
# Consistency and Standards

## Summary

**One-sentence:** Nielsen Heuristic #4: users should not wonder whether different words, situations, or actions mean the same thing.

**One-paragraph:** Nielsen Heuristic #4: users should not wonder whether different words, situations, or actions mean the same thing. Follow platform and industry conventions. Apply to audit visual, functional, and verbal consistency across a product, or to enforce design system compliance in code and component specs.

## Applies If (ALL must hold)

- Auditing a codebase or design for visual, functional, or verbal inconsistencies before a release
- Scanning UI copy across a product to surface synonym clusters and establish a canonical term glossary
- Reviewing a new component against an existing design system to flag deviations
- Enforcing design token usage in code (no hardcoded color or spacing values)

## Skip If (ANY kills it)

- Intentional brand differentiation from convention — consistency auditing does not adjudicate that decision
- Brand-new products with no design system — nothing to be consistent against yet
- Single-screen tools where cross-screen consistency is irrelevant

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

- parent skill: `solo/ux/ux-ui-designer/`
