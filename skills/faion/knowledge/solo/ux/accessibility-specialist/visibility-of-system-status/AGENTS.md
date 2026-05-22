---
slug: visibility-of-system-status
tier: solo
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The design must always keep users informed about what is going on through appropriate feedback within a reasonable amount of time.
content_id: "72c49c17b4a49c88"
tags: [usability, heuristics, feedback, loading, accessibility]
---
# Visibility of System Status

## Summary

**One-sentence:** The design must always keep users informed about what is going on through appropriate feedback within a reasonable amount of time.

**One-paragraph:** The design must always keep users informed about what is going on through appropriate feedback within a reasonable amount of time. Without system status visibility, users click repeatedly, abandon tasks, and lose trust. Feedback for every action, timely response, clear communication, and appropriate context are the core principles.

## Applies If (ALL must hold)

- Any user action that triggers a server request: form submissions, file uploads, payments, deletions
- Long-running operations (greater than 1 second): imports, exports, report generation, AI completions
- Asynchronous operations where the result arrives later: email send, background job, webhook
- Multi-step forms where users need to know which step they are on and how many remain
- Real-time status changes: connection health, sync state, auto-save confirmation

## Skip If (ANY kills it)

- Instantaneous operations (less than 100ms) where a loading indicator would flash and disappear distractingly
- Background telemetry or logging operations the user has no reason to know about
- Internal system operations that do not affect the user's current task

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

- parent skill: `solo/ux/accessibility-specialist/`
