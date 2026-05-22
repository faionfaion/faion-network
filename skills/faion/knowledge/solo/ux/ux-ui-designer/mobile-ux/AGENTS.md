---
slug: mobile-ux
tier: solo
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Mobile UX requires mobile-first design (smallest screen first, then enhance), touch targets of at least 44x44pt (iOS) or 48x48dp (Android), primary actions in the thumb zone (bottom third of screen), and Core Web Vitals targets of LCP < 2.
content_id: "88037c489f196607"
tags: [mobile, ux-design, touch-targets, performance, core-web-vitals]
---
# Mobile UX Design Basics

## Summary

**One-sentence:** Mobile UX requires mobile-first design (smallest screen first, then enhance), touch targets of at least 44x44pt (iOS) or 48x48dp (Android), primary actions in the thumb zone (bottom third of screen), and Core Web Vitals targets of LCP < 2.

**One-paragraph:** Mobile UX requires mobile-first design (smallest screen first, then enhance), touch targets of at least 44x44pt (iOS) or 48x48dp (Android), primary actions in the thumb zone (bottom third of screen), and Core Web Vitals targets of LCP < 2.5s / CLS < 0.1. Navigation defaults to bottom tab bar (3-5 items); hamburger menus are secondary. One primary action per screen is a hard constraint.

## Applies If (ALL must hold)

- Starting a product or feature that must run on mobile (apply mobile-first from the design phase).
- Auditing an existing web product for mobile usability issues before a campaign or launch.
- Reviewing PRs that add UI components to ensure touch targets, input types, and thumb-zone placement are correct.
- Before App Store or Google Play submission — checklist sweep against HIG and Material Design guidelines.
- Performance audit for mobile: LCP, FID, CLS targets are more critical on mobile than desktop.

## Skip If (ANY kills it)

- Internal tools used exclusively on desktop (admin panels, dashboards accessed via VPN).
- Projects where mobile is explicitly out of scope for the current phase.
- Prototyping in high fidelity before mobile constraints are validated — wireframe mobile flows first.
- Accessibility-only audits — mobile UX overlaps but is not a replacement for dedicated a11y review.

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

- parent skill: `solo/ux/ux-ui-designer/`
