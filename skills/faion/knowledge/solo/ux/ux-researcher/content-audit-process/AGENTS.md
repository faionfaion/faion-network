---
slug: content-audit-process
tier: solo
group: ux
domain: ux-researcher
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A structured 6-step process for systematically inventorying and evaluating all content assets, assigning each item an action (Keep/Update/Consolidate/Rewrite/Remove/Review), and producing a prioritized report.
content_id: "dbd4b14420f726d3"
tags: [content-audit, content-strategy, inventory, seo, governance]
---
# Content Audit Process

## Summary

**One-sentence:** A structured 6-step process for systematically inventorying and evaluating all content assets, assigning each item an action (Keep/Update/Consolidate/Rewrite/Remove/Review), and producing a prioritized report.

**One-paragraph:** A structured 6-step process for systematically inventorying and evaluating all content assets, assigning each item an action (Keep/Update/Consolidate/Rewrite/Remove/Review), and producing a prioritized report. Triggers a crawler-based or manual inventory, applies multi-criteria scoring, and outputs concrete migration or cleanup recommendations.

## Applies If (ALL must hold)

- Before a site migration or CMS switch — avoid importing bad content to the new platform.
- When SEO is underperforming and the cause is unclear — old or duplicate content may be to blame.
- When users report finding outdated information — audit scope starts at the affected content type.
- After significant product or pricing changes — detect pages that reference stale information.
- Annually as content governance to prevent slow decay.

## Skip If (ANY kills it)

- For a single-page or micro-site with fewer than 20 content items — a full audit adds overhead without payoff; a manual review suffices.
- When there is no plan to act on findings — audit data decays quickly; run only when there is owner commitment to execute the action list.
- Mid-sprint as a reactive measure — plan as a dedicated project with tooling and stakeholder buy-in.

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

- parent skill: `solo/ux/ux-researcher/`
