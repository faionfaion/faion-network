---
slug: ai-assisted-accessibility
tier: geek
group: ux
domain: ux-ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Pipeline for WCAG 2.
content_id: "a0f551d07b2edb06"
tags: [accessibility, wcag, a11y-testing, compliance, automation]
---
# AI-Assisted Accessibility

## Summary

**One-sentence:** Pipeline for WCAG 2.

**One-paragraph:** Pipeline for WCAG 2.2 AA compliance using AI-enhanced automated scanning (axe-core, Lighthouse, pa11y) as the first pass, followed by manual assistive technology testing for interactive components and cognitive accessibility. Automated tools catch 60-70% of auditable issues; the remaining 30-40% require human + AT verification.

## Applies If (ALL must hold)

- Sprint includes new UI components that must meet WCAG 2.2 AA before merge
- Accessibility audit needed for an existing product with no prior testing baseline
- Small team without a dedicated accessibility specialist (AI augments coverage)
- Preparing a VPAT for enterprise procurement
- Video/audio content being published (ADA Title II 2026 captions/audio descriptions required)

## Skip If (ANY kills it)

- Treating AI overlay widgets as a substitute for fixing underlying code — overlays are not compliant solutions
- As the only testing method — automated tools miss 30-40% of issues
- Complex interactive patterns (drag-and-drop, data grids, custom widgets) — AI scoring is unreliable; manual AT testing required
- When user testing with people with disabilities is scheduled — do automated pass first, fix, then test with real users

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
