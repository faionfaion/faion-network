---
slug: error-recovery
tier: solo
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Nielsen Heuristic #9: error messages must state what happened, why it happened, and how to fix it in plain language, without error codes, without blaming the user.
content_id: "207312f33d6aa6e7"
tags: [error-messages, microcopy, usability, heuristic-9, accessibility]
---
# Help Users Recognize, Diagnose, and Recover from Errors

## Summary

**One-sentence:** Nielsen Heuristic #9: error messages must state what happened, why it happened, and how to fix it in plain language, without error codes, without blaming the user.

**One-paragraph:** Nielsen Heuristic #9: error messages must state what happened, why it happened, and how to fix it in plain language, without error codes, without blaming the user. Every error must offer a recovery path (button or link), not just a description. Inline placement next to the problematic element is required for form errors; system errors use modal or banner with a retry action.

## Applies If (ALL must hold)

- Auditing existing UI error messages for clarity and actionability before a release.
- Writing microcopy for form validation, network errors, 404 pages, and payment failures.
- Code review: checking that API error strings are user-presentable before surfacing in UI.
- When support tickets reveal users confused by a specific error message.
- Systematic pre-launch sweep of all error states in a feature.

## Skip If (ANY kills it)

- Preventing errors in the first place — use Heuristic #5 (Error Prevention) instead.
- Designing empty states or onboarding flows — different UX domain.
- Performance or reliability issues causing errors — fix the root cause, not the message.
- Silent background errors that auto-retry without user involvement.
- Good error messages cannot fix bad IA — if users reach the wrong place, clarity is irrelevant.

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
