---
slug: visibility-of-system-status
tier: solo
group: ux
domain: ux-ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Nielsen Heuristic #1: every user action must produce visible feedback within the appropriate time threshold — spinner for 1-3s, progress bar for 3-10s, progress bar with percentage and cancel for over 10s.
content_id: "72c49c17b4a49c88"
tags: [ux, accessibility, feedback, loading-states, nielsen]
---
# Visibility of System Status

## Summary

**One-sentence:** Nielsen Heuristic #1: every user action must produce visible feedback within the appropriate time threshold — spinner for 1-3s, progress bar for 3-10s, progress bar with percentage and cancel for over 10s.

**One-paragraph:** Nielsen Heuristic #1: every user action must produce visible feedback within the appropriate time threshold — spinner for 1-3s, progress bar for 3-10s, progress bar with percentage and cancel for over 10s. Every interactive element needs three implemented states: loading (disabled + visual indicator), success (confirmation), and error (message with recovery action). Disable the trigger element during async operations to prevent double-submission.

## Applies If (ALL must hold)

- Auditing any interactive UI where user actions trigger async operations (form submissions, file uploads, API calls)
- Code review: verifying every button, link, and form has loading, success, and error states
- Before a launch: sweep all user flows for dead-click moments where UI appears unresponsive
- When support tickets or session recordings show users double-clicking or resubmitting forms
- Designing real-time features (chat, live data, collaborative editing) requiring continuous state feedback

## Skip If (ANY kills it)

- Static informational pages with no interactive elements — nothing to communicate
- Background operations the user does not need to know about (cache refresh completing in under 100ms)
- Micro-interactions already covered by platform defaults (OS-level progress bars for file transfers)
- When audit findings for this heuristic are already documented and tracked — fix, don't re-audit

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
