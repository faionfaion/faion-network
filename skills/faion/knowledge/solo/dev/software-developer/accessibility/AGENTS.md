---
slug: accessibility
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: WCAG 2.
content_id: "db4276a0dedfedda"
tags: [accessibility, wcag, a11y, web-standards, inclusive-design]
---
# Accessibility (Web)

## Summary

**One-sentence:** WCAG 2.

**One-paragraph:** WCAG 2.1/2.2 AA compliance methodology for web UIs. Covers semantic HTML, ARIA usage (first rule: don't use ARIA), keyboard navigation, focus management, color contrast, form labeling, live regions, and automated testing with axe-core. Treat AA as the minimum for all public-facing work.

## Applies If (ALL must hold)

- All web development — treat WCAG 2.1 AA as the default minimum.
- Public-facing applications, e-commerce, fintech, healthcare, government, education.
- Components in a design system or library (fix once, benefit everywhere).
- Any flow tied to revenue — accessibility bugs convert into lost sales.

## Skip If (ANY kills it)

- Internal one-off scripts used by 1–2 people who do not use assistive tech (low ROI, still worth doing if cheap).
- Throwaway experimental prototypes — defer until validated.
- "Skip a11y" is rarely correct; the question is always which effort level, not whether.

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

- parent skill: `solo/dev/software-developer/`
