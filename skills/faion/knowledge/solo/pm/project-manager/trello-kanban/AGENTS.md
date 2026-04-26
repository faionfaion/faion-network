# Trello Kanban

## Summary

A visual, card-based kanban workflow on Trello: board structure with WIP-limited lists, card anatomy with labels and checklists, Butler automation for rule-based transitions, custom fields for story points and sprint tracking, and REST API integration for agent-driven card management. WIP limits are enforced by list-name convention and Butler rules — not automatically blocked by the platform.

## Why

Trello's simplicity makes it the lowest-friction kanban tool for small teams and non-technical stakeholders. Its REST API is straightforward, and Butler automation handles mechanical state transitions (all checklists complete → move to Done) so agents only need to trigger higher-level operations. The tradeoff: no native velocity charts, no dependency tracking, no built-in OKR layer.

## When To Use

- Team of 1–5 people needing a visual board with minimal setup overhead
- Stakeholders are non-technical and need to update the board without training
- Rapid prototyping or pre-MVP phases where flexibility beats structure
- Budget constraints: Trello Free covers up to ~10 boards (1 Power-Up per board)
- No cross-repository code traceability needed

## When NOT To Use

- Team is already on GitHub — GitHub Projects has native code integration; use that instead
- Complex dependency tracking needed — Trello has no native dependency visualization
- OKR or goal tracking required — Trello has no goals layer; use ClickUp or Linear
- Velocity metrics or burndown charts needed regularly — requires premium Power-Ups
- More than ~10 boards under Free plan (Power-Up limit of 1 per board on Free)

## Content

| File | What's inside |
|------|---------------|
| `content/01-board-setup.xml` | Board structure rules, list naming with WIP limits, label system, card anatomy, best practices |
| `content/02-automation.xml` | Butler rule patterns, button examples, API integration rules, agent-usage gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/card-feature.md` | Feature card template with user story, AC, technical notes, DoD checklist |
| `templates/card-bug.md` | Bug card template with steps to reproduce, severity, environment |
