---
slug: design-docs-big-tech
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Reference survey of design-document practices at Google, Amazon, Uber, Spotify, Stripe, Netflix, Microsoft, Airbnb, Shopify, and Atlassian.
content_id: "8eee902fa44c57cb"
tags: [design-docs, rfc, architecture, big-tech, sdd]
---
# Design Docs at Big Tech Companies

## Summary

**One-sentence:** Reference survey of design-document practices at Google, Amazon, Uber, Spotify, Stripe, Netflix, Microsoft, Airbnb, Shopify, and Atlassian.

**One-paragraph:** Reference survey of design-document practices at Google, Amazon, Uber, Spotify, Stripe, Netflix, Microsoft, Airbnb, Shopify, and Atlassian. Covers document names (RFC, ERD, 6-Pager, ADR), review formats, and the trigger rules for when a doc is required vs. optional. The core rule: write before coding; match document weight to change scope; always include "do nothing" as an alternative.

## Applies If (ALL must hold)

- Choosing a design doc format before starting a cross-team feature or architecture change
- Adapting an RFC/ERD process to your team's async culture and scale
- Using an LLM to draft initial structure from requirements (outlines and alternatives)
- Onboarding new engineers via existing design docs as primary reference material
- Deciding whether a change needs a 1-pager, full RFC, or no doc at all

## Skip If (ANY kills it)

- Bug fixes and features under 2 days — skip the doc, write code
- Purely internal team decisions with no cross-team impact
- When organizational context, team politics, or proprietary system details are critical — LLMs cannot supply these
- Post-implementation documentation — design docs must precede coding to be useful

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

- parent skill: `solo/sdd/sdd/`
