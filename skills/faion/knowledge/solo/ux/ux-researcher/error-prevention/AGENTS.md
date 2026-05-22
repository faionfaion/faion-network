---
slug: error-prevention
tier: solo
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Eliminate error-prone conditions before they occur using six strategies: constraints, defaults, suggestions, validation, confirmation, and affordances.
content_id: "63a5c419599d76c8"
tags: [error-prevention, form-design, input-validation, user-experience, heuristic-5]
---
# Error Prevention — Nielsen Heuristic #5

## Summary

**One-sentence:** Eliminate error-prone conditions before they occur using six strategies: constraints, defaults, suggestions, validation, confirmation, and affordances.

**One-paragraph:** Eliminate error-prone conditions before they occur using six strategies: constraints, defaults, suggestions, validation, confirmation, and affordances.

## Applies If (ALL must hold)

- Designing or auditing any form with consequential data (payments, account changes, orders).
- When form abandonment or submission error rates are high in analytics.
- When reviewing any destructive action (delete, cancel subscription, bulk operation) for whether it needs a confirmation step.
- When validating that input fields constrain or guide input to valid values only.
- When analytics or support data shows a high rate of form submission failures or abandonment.
- Before launching a flow that involves irreversible actions (delete, cancel subscription, bulk operations).
- When auditing an existing product for heuristic compliance (Nielsen Heuristic #5).
- When input data quality downstream is poor (corrupted records, broken emails, invalid dates) — trace back to missing front-end constraints.

## Skip If (ANY kills it)

- Do not add confirmation dialogs to routine or easily reversible actions — over-confirming trains users to dismiss dialogs without reading, defeating the purpose.
- Do not apply real-time validation to every field indiscriminately — aggressive inline errors before the user has finished typing increase frustration; validate on blur for most fields, on keypress only for password strength indicators.
- Do not use error prevention as a substitute for error recovery design — prevention reduces errors but cannot eliminate them; both heuristics (#5 and #9) must be addressed.
- Do not apply prevention patterns to read-only interfaces with no user input — prevention patterns are irrelevant without user input.
- Do not make confirmation dialogs the default response to every action — overuse trains users to dismiss without reading.

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
