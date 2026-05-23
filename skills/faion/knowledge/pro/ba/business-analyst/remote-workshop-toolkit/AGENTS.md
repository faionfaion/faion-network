---
slug: remote-workshop-toolkit
tier: pro
group: ba
domain: ba
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Run-book for remote/hybrid BA workshops (pre-read floor, four-role breakouts, camera policy, time-zone split, async pulses) producing the workshop run-book + canvas templates + ground rules block.
content_id: "3220f6daae9d5ab1"
complexity: medium
produces: config
est_tokens: 4700
tags: [remote-workshop, business-analyst, facilitation, miro, figjam, hybrid]
---
# Remote Workshop Toolkit

## Summary

**One-sentence:** Run-book for remote/hybrid BA workshops (pre-read floor, four-role breakouts, camera policy, time-zone split, async pulses) producing the workshop run-book + canvas templates + ground rules block.

**One-paragraph:** Operating manual for remote and hybrid BA workshops — pre-reads, Miro/FigJam patterns, breakout protocol, time-zone splitting, on-camera ground rules, async pulses — so requirements work survives the lack of a shared room. Each workshop produces a typed run-book object satisfying the output contract.

**Ефективно для:**

- Remote / hybrid workshops з лезом проти lurker problem.
- Cross-time-zone cohort з ≥3 zones — split або async relay.
- Canvas-collaboration workshops (process map, story map, event storming).
- Series workshops, де треба переносити pre-read floor + ground rules.

## Applies If (ALL must hold)

- Remote-only or hybrid BA workshop with ≥4 attendees.
- Distributed team across ≥3 time zones (need split or async relay).
- Process / requirements work where canvas collaboration is the deliverable.
- Workshop with mixed stakeholder groups (sponsor + operator + engineering).
- Series of workshops sharing pre-read floor and ground rules.

## Skip If (ANY kills it)

- Single-room workshop where everyone is co-located.
- 1:1 interview — use elicitation-techniques instead.
- Decision meeting — use decision-analysis.
- Ad-hoc 30-min sync — overhead unjustified.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Workshop objective | Markdown | BA / facilitator |
| Stakeholder grid | JSON | stakeholder-analysis |
| Canvas tool credentials | env | infra |
| Pre-read draft | Markdown | BA |
| Calendar slots | ics | scheduling |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `pro/ba/business-analyst/elicitation-techniques` | Workshop technique uses this toolkit. |
| `pro/ba/business-analyst/scope-creep-parking-lot-protocol` | Parking-lot canvas integrated for ad-hoc asks. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules with rationale + source citations | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artefact + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | ~900 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pre_read_draft_from_brief` | sonnet | Bounded summarisation + framing. |
| `breakout_grouping_proposal` | sonnet | Apply stakeholder grid; produce groups of 4–6. |
| `canvas_layout_for_workshop_type` | haiku | Template selection by workshop type. |
| `async_pulse_question_set` | haiku | 3–5 quick questions per pulse. |
| `read_out_summary_synthesis` | sonnet | Combine breakout outputs into a coherent read-out. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pre-read.md` | 1–2 page pre-read structure. |
| `templates/miro-canvas-process-map.json` | Importable canvas for as-is/to-be process mapping. |
| `templates/miro-canvas-story-map.json` | Story-map canvas (backbone + walking skeleton). |
| `templates/miro-canvas-event-storming.json` | Big-picture event-storming canvas. |
| `templates/ground-rules.md` | Camera, mic, chat, hand-raise, breakout conventions. |
| `templates/async-pulse.md` | 5-min Loom or written pulse questionnaire. |
| `templates/_smoke-test.md` | Minimum filled-in run-book. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-remote-workshop-toolkit.py` | Validate the produced artefact against the output-contract schema. | Pre-commit; CI on each artefact change. |

## Related

- [[elicitation-techniques]]
- [[scope-creep-parking-lot-protocol]]
- [[decision-analysis]]
- [[modern-ba-framework]]

## Decision tree

See `content/06-decision-tree.xml`. The mandatory tree maps observable signals (engagement type, perspective set, scope, audit needs, baseline presence) to a single rule from `01-core-rules.xml`; every leaf references either a numbered core rule or the `skip-this-methodology` conclusion that routes the agent to a different methodology when this one does not apply.
