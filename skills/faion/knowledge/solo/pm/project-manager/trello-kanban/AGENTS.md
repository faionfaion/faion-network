---
slug: trello-kanban
tier: solo
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A visual, card-based kanban workflow on Trello: board structure with WIP-limited lists, card anatomy with labels and checklists, Butler automation for rule-based transitions, custom fields for story points and sprint tracking, and REST API integration for agent-driven card management.
content_id: "3062f115860d560f"
tags: [trello, kanban, project-management, automation, api]
---
# Trello Kanban

## Summary

**One-sentence:** A visual, card-based kanban workflow on Trello: board structure with WIP-limited lists, card anatomy with labels and checklists, Butler automation for rule-based transitions, custom fields for story points and sprint tracking, and REST API integration for agent-driven card management.

**One-paragraph:** A visual, card-based kanban workflow on Trello: board structure with WIP-limited lists, card anatomy with labels and checklists, Butler automation for rule-based transitions, custom fields for story points and sprint tracking, and REST API integration for agent-driven card management. WIP limits are enforced by list-name convention and Butler rules — not automatically blocked by the platform.

## Applies If (ALL must hold)

- Team of 1–5 people needing a visual board with minimal setup overhead
- Stakeholders are non-technical and need to update the board without training
- Rapid prototyping or pre-MVP phases where flexibility beats structure
- Budget constraints: Trello Free covers up to ~10 boards (1 Power-Up per board)
- No cross-repository code traceability needed

## Skip If (ANY kills it)

- Team is already on GitHub — GitHub Projects has native code integration; use that instead
- Complex dependency tracking needed — Trello has no native dependency visualization
- OKR or goal tracking required — Trello has no goals layer; use ClickUp or Linear
- Velocity metrics or burndown charts needed regularly — requires premium Power-Ups
- More than ~10 boards under Free plan (Power-Up limit of 1 per board on Free)

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

- parent skill: `solo/pm/project-manager/`
