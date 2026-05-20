---
slug: frontend-design
tier: solo
group: dev
domain: frontend-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A four-phase workflow for UI surfaces where multiple visual directions are explored before committing: (1) capture requirements (type, style, tech), (2) brainstorm 3–5 distinct variants via agent into designs/variant-N-slug/, each with working code and a rationale, (3) user selects and refines, (4) Storybook agent builds stories and component agent finalizes typed components.
content_id: "5ae6e00f1000265b"
tags: [design, variant-exploration, ui-design, brainstorming, storybook]
---
# Frontend Design Variant Exploration

## Summary

**One-sentence:** A four-phase workflow for UI surfaces where multiple visual directions are explored before committing: (1) capture requirements (type, style, tech), (2) brainstorm 3–5 distinct variants via agent into designs/variant-N-slug/, each with working code and a rationale, (3) user selects and refines, (4) Storybook agent builds stories and component agent finalizes typed components.

**One-paragraph:** A four-phase workflow for UI surfaces where multiple visual directions are explored before committing: (1) capture requirements (type, style, tech), (2) brainstorm 3–5 distinct variants via agent into designs/variant-N-slug/, each with working code and a rationale, (3) user selects and refines, (4) Storybook agent builds stories and component agent finalizes typed components. Variants must differ in typeface, density, color, and motion — not just palette.

## Applies If (ALL must hold)

- Starting a new UI surface (landing, dashboard, form, component set) with no visual decisions yet.
- Solo dev or small team wanting LLM-driven design exploration before implementation.
- Requirements exist but visual direction does not; brainstorming variants accelerates kickoff.
- Storybook is the deliverable — each variant must be explorable in isolation.

## Skip If (ANY kills it)

- Existing product with a mature design system — converging is more important than diverging.
- One-off internal tool where any reasonable UI suffices.
- Marketing pages where copy and photography drive design more than component patterns.
- Strict brand guideline enforcement: variant exploration generates ineligible options.

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
