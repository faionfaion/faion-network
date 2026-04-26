# Flexibility and Efficiency of Use

## Summary

Nielsen's Usability Heuristic #7: design must serve both novice and expert users. Accelerators (keyboard shortcuts, batch operations, command palettes, customization) speed up expert workflows while remaining invisible to novices. A command palette (Ctrl+K / Cmd+K) is the single best surface for making accelerators discoverable to both user types.

## Why

Interfaces designed only for novices frustrate power users who repeat the same actions daily. Interfaces designed only for experts overwhelm newcomers. The novice/expert spectrum is the most consistent source of usability complaints in productivity software; serving both requires layered affordances.

## When To Use

- Auditing a feature spec or UI for missing keyboard shortcuts, batch operations, and power-user accelerators
- Reviewing shortcut schemes for consistency with platform conventions (Mac/Windows/web)
- Identifying progressive disclosure opportunities: hiding advanced options without affecting novice users
- Code review: checking that CLI/API operations match UI operations (agent-accessibility parity)
- Generating a Flexibility Audit report from an action inventory

## When NOT To Use

- Product serves a single narrow use case with one user type — novice/expert design is unnecessary overhead
- Very early wireframing — flexibility patterns are implementation-level concerns, not concept-level
- Consumer mobile apps with infrequent use — most mobile users are perpetual novices; keyboard shortcuts do not apply
- When the bottleneck is latency, not interaction speed — shortcuts do not help if actions are slow

## Content

| File | What's inside |
|------|---------------|
| `content/01-patterns.xml` | Flexibility mechanisms, keyboard shortcut layering, progressive disclosure, accelerator types |
| `content/02-rules.xml` | Concrete rules, platform convention requirements, measuring efficiency, agent gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/flexibility-audit.md` | Audit table: action × shortcut/multi-path/batch/customization + recommendations |
| `templates/find-shortcuts.sh` | Bash script to extract all keyboard event listeners from a JS/TS codebase |
