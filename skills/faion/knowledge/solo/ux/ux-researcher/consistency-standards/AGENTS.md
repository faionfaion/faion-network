---
slug: consistency-standards
tier: solo
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Nielsen's Usability Heuristic #4: users should not have to wonder whether different words, situations, or actions mean the same thing.
content_id: "053ef7e57ea7ee24"
tags: [consistency, design-system, usability, heuristics, audit]
---
# Consistency and Standards

## Summary

**One-sentence:** Nielsen's Usability Heuristic #4: users should not have to wonder whether different words, situations, or actions mean the same thing.

**One-paragraph:** Nielsen's Usability Heuristic #4: users should not have to wonder whether different words, situations, or actions mean the same thing. Apply in five layers — internal, external, visual, functional, and verbal — prioritizing industry conventions over product-specific ones. Enforce through a design system and regular consistency audits that count distinct variations of each UI element.

## Applies If (ALL must hold)

- When starting a design system from scratch — define the consistency hierarchy before building components.
- When auditing an existing product for usability issues — inconsistency is often the root cause of user confusion.
- When onboarding a new designer or developer — the design system is the reference.
- Before a brand refresh — audit all touchpoints against the new standards before shipping.

## Skip If (ANY kills it)

- When intentional differentiation is the goal — e.g., a destructive action that must look visually distinct from standard actions. Purposeful inconsistency for contrast is valid.
- In early-stage exploration where standards have not been established — do not prematurely lock in patterns before validating with users.

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

- parent skill: `solo/ux/ux-researcher/`
