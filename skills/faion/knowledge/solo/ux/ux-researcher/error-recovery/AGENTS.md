---
slug: error-recovery
tier: solo
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Plain language error messages with three components: what happened, why, how to fix it.
content_id: "207312f33d6aa6e7"
tags: [error-recovery, error-messages, user-guidance, microcopy, heuristic-9]
---
# Error Recovery — Nielsen Heuristic #9

## Summary

**One-sentence:** Plain language error messages with three components: what happened, why, how to fix it.

**One-paragraph:** Plain language error messages with three components: what happened, why, how to fix it.

## Applies If (ALL must hold)

- Auditing any form, API response surface, or system state where errors can occur.
- Writing microcopy for validation errors, system failures, 404 pages, network errors.
- During a design review for any new feature that has failure states.
- When support ticket analysis reveals recurring user confusion about a specific error.

## Skip If (ANY kills it)

- Do not conflate error recovery with error prevention — prevention (Heuristic #5) eliminates errors before they occur; this methodology handles errors that do occur. Apply both, not one instead of the other.
- Do not use for success or informational states — the three-component structure (what/why/fix) is specific to failure states.

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
