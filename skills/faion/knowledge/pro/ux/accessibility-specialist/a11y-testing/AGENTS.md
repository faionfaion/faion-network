---
slug: a11y-testing
tier: pro
group: ux
domain: accessibility-specialist
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Five-step accessibility testing process combining automated scanning (axe, WAVE, Lighthouse, Pa11y), manual keyboard testing, screen reader verification, cognitive accessibility checks, and prioritized issue documentation.
content_id: "98f034ff4fd5f42f"
tags: [accessibility, testing, a11y, screen-readers, wcag]
---
# Accessibility Testing Process

## Summary

**One-sentence:** Five-step accessibility testing process combining automated scanning (axe, WAVE, Lighthouse, Pa11y), manual keyboard testing, screen reader verification, cognitive accessibility checks, and prioritized issue documentation.

**One-paragraph:** Five-step accessibility testing process combining automated scanning (axe, WAVE, Lighthouse, Pa11y), manual keyboard testing, screen reader verification, cognitive accessibility checks, and prioritized issue documentation. Automated tools catch ~30-40% of WCAG violations; the rest require structured manual walkthroughs with real AT.

## Applies If (ALL must hold)

- Pre-release WCAG 2.1/2.2 audit on a web product
- CI gate for new pages or components — automated scan must pass before merge
- Quarterly compliance review for ADA Title II or EAA-bound products
- Procurement: generating VPAT/ACR evidence from real test runs
- Triage: converting a raw a11y issue dump into a prioritized remediation plan

## Skip If (ANY kills it)

- Design-stage review — use accessibility-first-design (cheaper to fix in Figma than in code)
- Native mobile-only flows — axe/Pa11y do not cover XCUITest/Espresso; use platform-specific scanners
- XR/spatial interfaces — WCAG does not fully cover them; use spatial-accessibility and W3C XAUR
- Quick one-off contrast tweak — run Colour Contrast Analyser directly, not a full audit

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
