---
slug: trello-kanban
tier: solo
group: pm
domain: pm
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Solo / small-team Trello kanban setup: 5-column board, WIP limits, label taxonomy, Power-Ups budget, automation rules.
content_id: "3062f115860d560f"
complexity: medium
produces: spec
est_tokens: 3700
tags: ["trello", "kanban", "pm-agile", "pm", "solo"]
---
# Trello Kanban

## Summary

**One-sentence:** Solo / small-team Trello kanban setup: 5-column board, WIP limits, label taxonomy, Power-Ups budget, automation rules.

**One-paragraph:** Pins the Trello kanban baseline: one board, 5 named columns (Backlog / Ready / In Progress / Review / Done), WIP limits per column, ≤8 labels, ≤2 Power-Ups, basic Butler automation. Output is a versioned spec preventing the 30-column / 50-label rotting most Trello boards hit by month 6.

**Ефективно для:**

- Solo founder or small team running ops/sales/onboarding on Trello (not engineering — use Linear / Notion for that). Pins WIP limits + a curated label set so the board doesn't bloat into illegibility.

## Applies If (ALL must hold)

- Team uses Trello as primary tracker for an ops / sales / onboarding workflow
- Board has ≤2 lifecycle stages (not a meta-board)
- Team size 1-8 (Trello scales poorly above this)

## Skip If (ANY kills it)

- Engineering issue tracker — Linear / Notion are better fits
- Team size >10 — Trello UX degrades
- Workflow needs custom fields with strict validation (Trello custom fields are loose)

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Single workflow definition (lifecycle stages) | doc | ops doc |
| Team roster + Trello membership | table | Trello admin |
| Existing label set (if migrating) | list | current board |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/pm/project-manager/freelancer-personal-crm-minimal` | Peer methodology — CRM card pipeline lives on a similar board pattern. |
| `solo/pm/pm-agile/notion-pm` | Peer methodology — comparison baseline for tracking choice. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules incl. skip-this-methodology + run-the-checklist | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-trello-kanban` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-trello-kanban` | haiku | Schema check + threshold checks; deterministic. |
| `review-trello-kanban` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/trello-kanban.json` | JSON skeleton conforming to the output contract schema. |
| `templates/trello-kanban.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-trello-kanban.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[notion-pm]]
- [[freelancer-personal-crm-minimal]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
