---
slug: outcome-based-roadmaps-advanced
tier: solo
group: product
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Advanced outcome roadmapping closes the gap between high-level business goals and the product experiments that move them.
content_id: "12d3860c47dee210"
tags: [roadmap, outcome-decomposition, business-goals, product-strategy, stakeholder-communication, confidence-levels, experiments]
---
# Outcome-Based Roadmaps (Advanced)

## Summary

**One-sentence:** Advanced outcome roadmapping closes the gap between high-level business goals and the product experiments that move them.

**One-paragraph:** Advanced outcome roadmapping closes the gap between high-level business goals and the product experiments that move them. The autonomous-agent skill: take a stated business goal (e.g. "increase revenue 20%") and produce (a) a four-layer decomposition tree (Business Goal → Product Outcome → Leading Indicator → Experiment), (b) pre-registered success criteria for every experiment, (c) confidence labels (High / Medium / Low / Exploring) instead of dates, and (d) four audience-tailored roadmap artifacts (customer, board, engineering, sales) emitted from a single source of truth. Use this methodology whenever stakeholders demand specific features and dates while the team must own metric outcomes — the most common pressure scenario for product teams in 2026.

## Applies If (ALL must hold)

- Trigger A — Stakeholder pressure: a board member, sales lead, or customer demands "what features ship in Q2 with dates" while the team has agreed to outcome ownership. Run this methodology to convert the demand into an outcome conversation.
- Trigger B — OKR decomposition: the company has just published a quarterly or annual OKR (e.g. "increase ARR 20%") and the product team must translate it into experiments that could plausibly move it.
- Trigger C — Quarterly roadmap presentation: roadmap is due in N days for multiple audiences (board, customers, engineering, sales). Run this methodology to emit four artifacts from one source.
- Trigger D — Roadmap drift: features ship on schedule but business metrics do not move. Run this methodology to rebuild the roadmap around outcomes and force-rank by leading-indicator impact.
- Trigger E — After basic roadmap-design has been adopted but the team has not yet introduced outcome decomposition, leading indicators, or audience segmentation.

## Skip If (ANY kills it)

- Pre-PMF where there are no product outcomes to track yet — too early for decomposition. Use product-discovery and continuous-discovery instead.
- Compliance, regulatory, or operational work where the outcome is dictated by an external party, not hypothesized.
- Teams without any analytics instrumentation — outcome roadmaps require measurable leading indicators. Instrument first, then return.
- One-off internal tools or migrations where the success criterion is binary completion, not a metric movement.

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

- parent skill: `solo/product/product-planning/`
