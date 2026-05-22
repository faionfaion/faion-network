---
slug: accessibility-first-design
tier: pro
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Methodology for embedding accessibility requirements at the design stage — color contrast ratios, semantic structure, touch target sizing, motion controls, and focus management — before a single line of code is written.
content_id: "041bb0f6779595cb"
tags: [accessibility, a11y, design, wcag, inclusive-design]
---
# Accessibility-First Design

## Summary

**One-sentence:** Methodology for embedding accessibility requirements at the design stage — color contrast ratios, semantic structure, touch target sizing, motion controls, and focus management — before a single line of code is written.

**One-paragraph:** Methodology for embedding accessibility requirements at the design stage — color contrast ratios, semantic structure, touch target sizing, motion controls, and focus management — before a single line of code is written. The core rule: 70-80% of accessibility defects are preventable at design time; retrofitting costs far more than getting it right first.

## Applies If (ALL must hold)

- Starting a new UI design (web, mobile, or desktop)
- Adding a new component or page to an existing design system
- Conducting a design review before dev handoff
- Evaluating a Figma/Sketch file for accessibility gaps
- Writing design spec annotations for developers

## Skip If (ANY kills it)

- Post-production audits where design files no longer exist — use code-level audit tools (axe, Lighthouse) instead
- Back-end or API work with no visual output
- Content writing (separate content accessibility concerns apply)
- Late-stage retrofit of an existing product — use a11y-testing to find issues, then fix systematically

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

- parent skill: `pro/ux/accessibility-specialist/`
