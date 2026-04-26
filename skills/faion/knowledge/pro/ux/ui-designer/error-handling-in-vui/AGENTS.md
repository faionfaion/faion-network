# Error Handling in VUI

## Summary

Methodology for designing voice UI error recovery: a three-tier progressive disclosure sequence (simple retry → example phrases → modality switch) mapped to the four error types (no input, no match, ambiguous, system error). The core rule: never blame the user, always add new information on each retry, escalate to a different modality after two failures.

## Why

Voice recognition errors are unavoidable; the difference between a frustrating and a recoverable VUI is the error handling design. Repeating the same prompt after a failure provides no new information and drives abandonment. A structured escalation that offers examples and then switches modality (visual, agent) breaks the failure loop.

## When To Use

- Designing dialogue flows for any voice interface or voice assistant feature
- Writing error message scripts for VUI flows
- Auditing an existing VUI for error recovery patterns
- Specifying VUI behavior in design documentation for developers

## When NOT To Use

- Backend ASR model tuning — this methodology covers dialogue design, not model training
- GUI-only error handling — different methodology applies (form validation, toast notifications)
- Chatbot text error handling with no voice component

## Content

| File | What's inside |
|------|---------------|
| `content/01-error-recovery.xml` | Four error types, three-tier recovery sequence, dialogue examples, and antipatterns |

## Templates

none
