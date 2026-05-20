---
slug: user-control-freedom
tier: solo
group: ux
domain: ux-ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Nielsen's Usability Heuristic #3: every interface must provide clearly marked "emergency exits" — undo, cancel, back, close, and reset — so users can recover from mistakes without going through extended processes.
content_id: "e4904fae94ae0b47"
tags: [user-control, undo, heuristics, accessibility, modal-design]
---
# User Control and Freedom

## Summary

**One-sentence:** Nielsen's Usability Heuristic #3: every interface must provide clearly marked "emergency exits" — undo, cancel, back, close, and reset — so users can recover from mistakes without going through extended processes.

**One-paragraph:** Nielsen's Usability Heuristic #3: every interface must provide clearly marked "emergency exits" — undo, cancel, back, close, and reset — so users can recover from mistakes without going through extended processes. Prefer undo over confirmation dialogs for reversible actions; reserve confirmation only for irreversible, high-stakes operations.

## Applies If (ALL must hold)

- Heuristic audit of a feature spec or UI for missing undo/cancel/exit mechanisms
- Generating a User Control Audit report (action table with undo/cancel/exit columns)
- Code review: checking that destructive backend actions have soft-delete or undo hooks
- Accessibility review: verifying keyboard escape paths and focus management in modal flows
- Design review of multi-step wizards or onboarding flows for trapped-user patterns

## Skip If (ANY kills it)

- As a substitute for actual usability testing — structural absence of controls is detectable, but whether users feel trapped requires behavioral data
- Complex undo architecture in database-backed systems — engineering judgment on consistency and rollback scope is required
- When the system genuinely cannot support undo (sent emails, executed financial transactions) — the design solution (clear warnings) needs human decision

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
