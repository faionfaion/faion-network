---
slug: cognitive-inclusion-design
tier: pro
group: ux
domain: ux-ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A design methodology that reduces cognitive load and adapts interfaces for users with ADHD, autism spectrum, dyslexia, dyscalculia, anxiety, low literacy, and aging cognition through structural patterns (chunking, predictability, progress indicators) and optional settings (focus mode, dyslexia font, reduced motion, extended time limits).
content_id: "c1407cca3d3f9f7c"
tags: [accessibility, cognitive, inclusion, adhd, autism, dyslexia]
---
# Cognitive Inclusion Design

## Summary

**One-sentence:** A design methodology that reduces cognitive load and adapts interfaces for users with ADHD, autism spectrum, dyslexia, dyscalculia, anxiety, low literacy, and aging cognition through structural patterns (chunking, predictability, progress indicators) and optional settings (focus mode, dyslexia font, reduced motion, extended time limits).

**One-paragraph:** A design methodology that reduces cognitive load and adapts interfaces for users with ADHD, autism spectrum, dyslexia, dyscalculia, anxiety, low literacy, and aging cognition through structural patterns (chunking, predictability, progress indicators) and optional settings (focus mode, dyslexia font, reduced motion, extended time limits).

## Applies If (ALL must hold)

- Designing for users with ADHD, autism, dyslexia, dyscalculia, anxiety, low-literacy, or aging cognition.
- Adding plain-language, focus mode, reduced-motion, customizable text/layout, time-extension features.
- Reviewing flows where cognitive load is the dominant friction (forms, taxes, healthcare, legal, government).
- Aligning with WCAG 3.0 working draft cognitive guidelines and W3C COGA Task Force gap analysis.

## Skip If (ANY kills it)

- Pure visual / motor accessibility—handle via WCAG 2.2 AA + assistive-tech testing first.
- Marketing surfaces with single-action goals (CTA + form)—usually does not need cognitive customization.
- Highly regulated technical interfaces (industrial control) where literal labeling is already required.
- As a substitute for plain-language editing—cognitive design assumes content is already plain.

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
