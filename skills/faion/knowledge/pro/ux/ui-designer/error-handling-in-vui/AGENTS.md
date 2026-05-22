---
slug: error-handling-in-vui
tier: pro
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Voice recognition errors are unavoidable; the difference between a frustrating and a recoverable VUI is the error handling design.
content_id: "09b767fa3be9320a"
tags: [voice-ui, error-handling, dialogue-design, accessibility]
---
# Error Handling in VUI

## Summary

**One-sentence:** Voice recognition errors are unavoidable; the difference between a frustrating and a recoverable VUI is the error handling design.

**One-paragraph:** Voice recognition errors are unavoidable; the difference between a frustrating and a recoverable VUI is the error handling design. Repeating the same prompt after a failure provides no new information and drives abandonment. A structured escalation that offers examples and then switches modality (visual, agent) breaks the failure loop.

## Applies If (ALL must hold)

- Designing dialogue flows for any voice interface or voice assistant feature
- Writing error message scripts for VUI flows
- Auditing an existing VUI for error recovery patterns
- Specifying VUI behavior in design documentation for developers

## Skip If (ANY kills it)

- Backend ASR model tuning — this methodology covers dialogue design, not model training
- GUI-only error handling — different methodology applies (form validation, toast notifications)
- Chatbot text error handling with no voice component

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

- parent skill: `pro/ux/ui-designer/`
