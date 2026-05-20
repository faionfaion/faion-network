---
slug: flexibility-efficiency
tier: solo
group: ux
domain: ux-ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Accelerators (keyboard shortcuts, batch operations, command palettes) speed expert workflows while remaining invisible to novices.
content_id: "850eca43a1a85ff9"
tags: [keyboard-shortcuts, accelerators, usability, heuristic-7, power-users]
---
# Flexibility and Efficiency of Use

## Summary

**One-sentence:** Accelerators (keyboard shortcuts, batch operations, command palettes) speed expert workflows while remaining invisible to novices.

**One-paragraph:** Accelerators (keyboard shortcuts, batch operations, command palettes) speed expert workflows while remaining invisible to novices.

## Applies If (ALL must hold)

- Auditing a feature spec or UI for missing keyboard shortcuts, batch operations, and power-user accelerators.
- Reviewing shortcut schemes for consistency with platform conventions (Mac/Windows/web).
- Identifying progressive disclosure opportunities: hiding advanced options without affecting novice users.
- Code review: checking that CLI/API operations match UI operations (agent-accessibility parity).
- Generating a Flexibility Audit report from an action inventory.

## Skip If (ANY kills it)

- Product serves a single narrow use case with one user type — novice/expert design is unnecessary overhead.
- Very early wireframing — flexibility patterns are implementation-level concerns, not concept-level.
- Consumer mobile apps with infrequent use — most mobile users are perpetual novices; keyboard shortcuts do not apply.
- When the bottleneck is latency, not interaction speed — shortcuts do not help if actions are slow.

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
