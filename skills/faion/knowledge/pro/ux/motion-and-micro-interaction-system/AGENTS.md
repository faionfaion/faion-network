---
slug: motion-and-micro-interaction-system
tier: pro
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Motion tokens (durations, easings), prefers-reduced-motion, perceived performance, choreography between components — the motion methodology corpus has zero of.
content_id: "f9056668c6d378c0"
tags: [motion-and-micro-interaction-system, ux, pro]
---

# Motion and Micro-Interaction System

## Summary

**One-sentence:** Motion tokens (durations, easings), prefers-reduced-motion, perceived performance, choreography between components — the motion methodology corpus has zero of.

**One-paragraph:** Corpus has zero motion methodology. Motion tokens, reduced-motion, perceived performance, choreography — all missing. Output: motion token set + choreography rules + accessibility policy.

## Applies If (ALL must hold)

- product has UI (web, mobile, desktop)
- design system in place OR being established
- designer + frontend dev collaboration possible

## Skip If (ANY kills it)

- API-only / CLI-only product
- single-screen demo / one-off — overhead not justified
- team has motion designer + comprehensive system — augment, don't duplicate

## Prerequisites

- design tokens for color + spacing already established
- frontend stack supports CSS transitions / Framer Motion / Lottie / native animations
- a11y baseline (WCAG AA at minimum)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ux/ux-ui-designer` | parent skill — provides operating context for this methodology |
| `pro/ux/ux-ui-designer` | peer methodology — produces inputs or consumes outputs |
| `pro/ux/accessibility-specialist` | peer methodology — produces inputs or consumes outputs |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules | ~900 |
| `content/02-output-contract.xml` | essential | required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Related

- parent skill: `pro/ux/ux-ui-designer/`
- peer methodology: `pro/ux/ux-ui-designer`
- peer methodology: `pro/ux/accessibility-specialist`
- peer methodology: `pro/product/design-ops-foundations`
- external: https://material.io/design/motion/; https://www.lukew.com/ff/entry.asp?1797 (Luke W on motion); https://www.w3.org/WAI/WCAG21/Understanding/animation-from-interactions
