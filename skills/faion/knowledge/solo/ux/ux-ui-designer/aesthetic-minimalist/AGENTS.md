---
slug: aesthetic-minimalist
tier: solo
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Nielsen Heuristic #8: Interfaces should not contain information which is irrelevant or rarely needed.
content_id: "9b2a743aaacaba26"
tags: [ux, heuristics, minimalism, usability, visual-hierarchy]
---
# Aesthetic and Minimalist Design

## Summary

**One-sentence:** Nielsen Heuristic #8: Interfaces should not contain information which is irrelevant or rarely needed.

**One-paragraph:** Nielsen Heuristic #8: Interfaces should not contain information which is irrelevant or rarely needed. Every extra unit of information in an interface competes with the relevant units of information and diminishes their relative visibility. Apply content prioritization, progressive disclosure, visual hierarchy, and white space to eliminate clutter and let important elements stand out.

## Applies If (ALL must hold)

- Auditing an existing UI for visual clutter before a redesign sprint.
- Reviewing new feature additions to ensure they don't overload existing pages.
- Conducting a content audit to identify remove/hide/keep candidates.
- Evaluating dashboard and data-heavy screens where information overload is common.
- Mobile-first simplification passes where screen real estate is constrained.

## Skip If (ANY kills it)

- Data-dense tools (analytics dashboards, IDEs, spreadsheets) where density is a feature, not a bug.
- First-pass feature discovery sessions — minimalism audits assume features already exist and need pruning.
- When user research has not yet established which features are "rarely used" — guessing leads to removing the wrong things.
- Branding or marketing contexts where visual richness drives emotion, not utility.

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
