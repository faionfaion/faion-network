---
slug: user-control-freedom
tier: solo
group: ux
domain: ux-researcher
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Usability Heuristic #3: Users often perform actions by mistake.
content_id: "e4904fae94ae0b47"
tags: [heuristics, usability, control, undo, user-centered]
---
# User Control and Freedom

## Summary

**One-sentence:** Usability Heuristic #3: Users often perform actions by mistake.

**One-paragraph:** Usability Heuristic #3: Users often perform actions by mistake. They need a clearly marked "emergency exit" to leave the unwanted action without having to go through an extended process. Implement undo and redo, cancel buttons, back navigation, and forgiving design patterns so users recover from mistakes without feeling trapped.

## Applies If (ALL must hold)

- Designing any state-changing action (delete, archive, update, subscribe, publish)—ask "Can the user undo this?"
- Building multi-step workflows or wizards—ensure back navigation and exit points at every step.
- Creating modals or dialogs—ensure users can close via X button, Escape key, and clicking outside.
- Designing destructive actions (delete, permanent removal)—use soft delete (trash with retention) before confirmation dialogs.
- Auditing an existing UI for missing undo/cancel affordances—apply this heuristic during quality gates.

## Skip If (ANY kills it)

- When designing intentionally irreversible flows (legal e-signature, financial commit, account deletion)—those require explicit confirmation, not undo, and should be rare.
- When content is already fully auto-saved and loss is impossible—undo adds noise without value.
- As a substitute for full heuristic evaluation—run all 10 Nielsen heuristics together for comprehensive audit.
- On a UI that is purely read-only with no state changes.

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
