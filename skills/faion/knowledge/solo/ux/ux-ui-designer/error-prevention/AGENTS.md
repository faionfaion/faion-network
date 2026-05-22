---
slug: error-prevention
tier: solo
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Nielsen Heuristic #5: design out error conditions before they occur.
content_id: "63a5c419599d76c8"
tags: [error-prevention, validation, forms, ux-heuristics, usability]
---
# Error Prevention

## Summary

**One-sentence:** Nielsen Heuristic #5: design out error conditions before they occur.

**One-paragraph:** Nielsen Heuristic #5: design out error conditions before they occur. Apply constraints, defaults, inline validation, and confirmation dialogs instead of error messages.

## Applies If (ALL must hold)

- Auditing form specs for missing input constraints, absent real-time validation, or unguarded destructive actions
- Reviewing API endpoint contracts for inputs accepted without server-side constraints
- Drafting confirmation dialog copy for delete, cancel-subscription, or bulk operations
- Reviewing code PRs for validation gaps: fields that accept any string where a constrained type is appropriate

## Skip If (ANY kills it)

- Replacing QA — error prevention is a design heuristic, not a test suite
- Adding confirmations to routine, easily reversible actions — dialog fatigue reduces effectiveness for genuinely dangerous actions
- Very early concept stage where form fields are not yet defined

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
