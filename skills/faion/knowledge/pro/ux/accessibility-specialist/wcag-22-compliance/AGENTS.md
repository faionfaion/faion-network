---
slug: wcag-22-compliance
tier: pro
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Delta methodology for upgrading from WCAG 2.
content_id: "fcb092b185dfceb7"
tags: [wcag, wcag-2-2, accessibility, compliance, a11y]
---
# WCAG 2.2 Compliance

## Summary

**One-sentence:** Delta methodology for upgrading from WCAG 2.

**One-paragraph:** Delta methodology for upgrading from WCAG 2.0/2.1 to 2.2 (published October 2023). Covers all 9 new success criteria, the removal of 4.1.1 Parsing, and the 5 new AA-level criteria most teams miss: 2.4.11 Focus Not Obscured, 2.5.7 Dragging Movements, 2.5.8 Target Size (24x24 CSS px minimum), 3.3.7 Redundant Entry, and 3.3.8 Accessible Authentication.

## Applies If (ALL must hold)

- Auditing or upgrading a product from WCAG 2.0/2.1 to 2.2.
- Implementing WCAG 2.2 AA criteria in new components (drag, auth, multi-step forms).
- Writing acceptance criteria that reference 2.2 SC numbers.
- Future-proofing for ADA Title II extensions and EU EAA (EN 301 549 will incorporate 2.2).

## Skip If (ANY kills it)

- General a11y triage on a new codebase — start with `a11y-testing` or `a11y-basics`.
- AT runtime testing — use `testing-with-assistive-technology`.
- Compliance paperwork / VPAT — use `regulatory-compliance-2026`.
- XR/spatial products — use `spatial-accessibility`; WCAG 2.2 does not fully cover them.

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
