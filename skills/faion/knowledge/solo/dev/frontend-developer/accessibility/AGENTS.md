---
slug: accessibility
tier: solo
group: dev
domain: frontend-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Web accessibility: make interfaces perceivable, operable, understandable, and robust for all users including those using assistive technologies.
content_id: "db4276a0dedfedda"
tags: [accessibility, wcag, aria, a11y, semantic-html]
---
# Accessibility (WCAG)

## Summary

**One-sentence:** Web accessibility: make interfaces perceivable, operable, understandable, and robust for all users including those using assistive technologies.

**One-paragraph:** Web accessibility: make interfaces perceivable, operable, understandable, and robust for all users including those using assistive technologies. WCAG 2.1/2.2 AA is the target conformance level. Accessibility is a default practice, not an opt-in feature.

## Applies If (ALL must hold)

- Every web project — accessibility is a default, not an opt-in.
- Public-facing apps subject to ADA, EAA (June 2025 EU mandate), Section 508, AODA.
- Enterprise/government RFPs that require WCAG 2.1 AA or 2.2 AA conformance.
- E-commerce and fintech where assistive-tech failures convert directly into lost revenue + lawsuits.
- Any agent-generated UI: LLMs systematically under-deliver on a11y unless forced.

## Skip If (ANY kills it)

- Internal CLI/server-only tools with no UI surface (still apply for any web admin panel).
- Throwaway experiments — but even then, accessible markup is rarely more expensive than div soup.

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
