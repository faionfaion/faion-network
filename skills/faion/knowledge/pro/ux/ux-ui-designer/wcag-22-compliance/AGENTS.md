---
slug: wcag-22-compliance
tier: pro
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: WCAG 2.
content_id: "fcb092b185dfceb7"
tags: [wcag, accessibility, compliance, a11y, standards]
---
# WCAG 2.2 Compliance

## Summary

**One-sentence:** WCAG 2.

**One-paragraph:** WCAG 2.2 released October 2023, baseline compliance standard by 2025-2026. Covers nine new success criteria including focus visibility, target size, drag alternatives, and accessible authentication.

## Applies If (ALL must hold)

- Validating a web product against WCAG 2.2 AA — the global baseline by 2025/2026.
- Adding a CI gate that flags new violations of the nine WCAG 2.2 success criteria added on top of 2.1.
- Auditing focus visibility, target size, dragging, accessible authentication, redundant entry, consistent help.
- Preparing VPAT 2.5 / ACR conformance documentation.

## Skip If (ANY kills it)

- Native mobile-only apps without web surfaces — defer to platform a11y APIs (UIAccessibility, Android a11y).
- Internal tooling with a documented narrow user pool that does not include disabled users (rare; document the decision).
- WCAG 3.0 silver-bullet conversations — 3.0 is still working draft; do not retire 2.2 baselines.
- Pure visual design review — heuristics and cognitive walkthrough cover that better.

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
