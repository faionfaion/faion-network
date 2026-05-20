---
slug: onboarding-flows
tier: pro
group: marketing
domain: conversion-optimizer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A design framework for guiding new users from signup to their first "Aha moment" as fast as possible.
content_id: "4fc19f5ba3b052d8"
tags: [onboarding, user-activation, saas, funnel-optimization, flow-design]
---
# User Onboarding Flow Design

## Summary

**One-sentence:** A design framework for guiding new users from signup to their first "Aha moment" as fast as possible.

**One-paragraph:** A design framework for guiding new users from signup to their first "Aha moment" as fast as possible. Core principle: show value before asking for work. Segment users at signup (one question), route each segment to a matching pattern (template-first / wizard / interactive / self-serve / concierge), cap the critical path at 3-5 required steps, and pair every in-app step with a triggered email that stops the moment the user activates.

## Applies If (ALL must hold)

- Designing or rebuilding the first-run experience for a SaaS product where activation rate is below 50%.
- Choosing among onboarding patterns (template-first, wizard, interactive tutorial, self-serve, concierge) for a specific product.
- Reducing step count without losing necessary configuration.
- Adding progressive disclosure, contextual tooltips, and progress checklists to an existing flow.
- Coordinating in-app guidance with a triggered email sequence for the same activation goal.

## Skip If (ANY kills it)

- The activation event is not yet defined — pause and run activation analysis first.
- Pre-PMF startups where onboarding optimization masks a value-prop problem.
- Enterprise products with bespoke deal-by-deal onboarding — focus on Customer Success playbooks instead.
- Products with extremely simple value (no setup needed) — over-engineered onboarding hurts more than it helps.

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

- parent skill: `pro/marketing/conversion-optimizer/`
