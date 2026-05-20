---
slug: mobile-responsive
tier: solo
group: dev
domain: frontend-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Mobile-first responsive design: base styles are unconditional (mobile), min-width queries layer up for larger screens.
content_id: "70d07f8d3bcdef0c"
tags: [responsive-design, mobile-first, css, container-queries, accessibility]
---
# Mobile-First Responsive Design

## Summary

**One-sentence:** Mobile-first responsive design: base styles are unconditional (mobile), min-width queries layer up for larger screens.

**One-paragraph:** Mobile-first responsive design: base styles are unconditional (mobile), min-width queries layer up for larger screens. Breakpoints are derived from content, not device names. clamp() replaces stepwise media queries for typography and spacing. Container queries (@container) replace viewport queries inside components. Touch targets meet WCAG 2.5.8 minimum of 44x44 CSS px.

## Applies If (ALL must hold)

- Greenfield site/app — set viewport meta, mobile-first base CSS, container queries from the first commit.
- Auditing an existing layout for breakpoint regressions, touch-target sizes, and CLS on small screens.
- Migrating from viewport-based to container-query-based responsive design.
- Configuring Tailwind breakpoints to match real content breakpoints, not device widths.

## Skip If (ANY kills it)

- App is locked to a single device class (kiosk, tablet-only internal tool) — fixed layout is simpler.
- Framework already enforces mobile-first and the site passes Lighthouse mobile — adding breakpoints is busywork.

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

- parent skill: `solo/dev/frontend-developer/`
