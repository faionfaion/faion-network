---
slug: cognitive-inclusion-design
tier: pro
group: ux
domain: accessibility-specialist
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Design patterns for cognitive accessibility: ADHD, autism, dyslexia, anxiety, learning disabilities (15-20% of population).
content_id: "c1407cca3d3f9f7c"
tags: [cognitive-accessibility, neurodiversity, adhd, autism, dyslexia]
---
# Cognitive Inclusion Design

## Summary

**One-sentence:** Design patterns for cognitive accessibility: ADHD, autism, dyslexia, anxiety, learning disabilities (15-20% of population).

**One-paragraph:** Design patterns for cognitive accessibility: ADHD, autism, dyslexia, anxiety, learning disabilities (15-20% of population). Auto-save, progress indicators, predictable navigation, plain language, dyslexia-friendly typography, reduced-motion defaults, non-blaming errors, sensory-friendly modes.

## Applies If (ALL must hold)

- Designing or auditing forms, dashboards, learning tools, government services, or healthcare apps used by a non-expert public.
- Reducing form abandonment or support load on complex multi-step flows.
- Auditing copy, error messages, and microcopy for plain language and non-blaming tone.
- Working in EU (EAA) where WCAG 2.2 AA + cognitive guidance is expected.
- Accommodating neurodiverse employees in internal tools (HR platforms, intranets).

## Skip If (ANY kills it)

- Pure visual/motor a11y audit — use `a11y-testing` and `wcag-22-compliance`.
- Performance-driven, expert-only tooling (CLI dashboards for SREs) — minimalism trumps scaffolding.
- Marketing landing pages where brand voice is intentionally playful — idioms acceptable in moderation.
- Game design where challenge is the point — apply selectively (settings menu, onboarding only).

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
