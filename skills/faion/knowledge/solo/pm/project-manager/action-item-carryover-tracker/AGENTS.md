---
slug: action-item-carryover-tracker
tier: solo
group: pm
domain: pm
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Single rolling log of action items + carryover age + owner + due date — surfaces 'this thing has slipped 4 weeks' before the meeting dies.
content_id: "e32d17bb20881a98"
complexity: medium
produces: report
est_tokens: 3700
tags: ["action-items", "pm", "solo", "meetings", "tracker"]
---
# Action Item Carryover Tracker

## Summary

**One-sentence:** Single rolling log of action items + carryover age + owner + due date — surfaces 'this thing has slipped 4 weeks' before the meeting dies.

**One-paragraph:** Pins a rolling action-item log indexed by source meeting + owner + due date + carryover age. Output is a versioned spec; weekly the agent emits the 'stale' subset (carryover ≥3) to force triage instead of theatre.

**Ефективно для:**

- Solo founder running meetings whose 'action items' line gets longer each week. Surfaces stale items (≥3 carryovers) so they're killed, closed, or escalated — not silently re-added.

## Applies If (ALL must hold)

- ≥1 recurring meeting generating action items
- Team / founder reviews meeting notes ≥weekly
- Action items have identifiable owners (even if same person)

## Skip If (ANY kills it)

- Solo no-meeting founder with no recurring action-item source
- Action items already tracked rigorously in PM tool (Linear / Asana)
- Crisis-incident mode — actions captured per-incident

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Source meeting list (standup / 1:1 / sprint review) | table | calendar |
| Existing action-item dumps from last 4 weeks | doc | meeting notes |
| Owner identifier convention (@handle) | doc | team agreement |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/pm/async-standup-methodology` | Peer methodology — async standup feeds blocker actions into this tracker. |
| `solo/pm/burndown-diagnosis-cheatsheet` | Peer methodology — remediation actions land here. |

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
| `draft-action-item-carryover-tracker` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-action-item-carryover-tracker` | haiku | Schema check + threshold checks; deterministic. |
| `review-action-item-carryover-tracker` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/action-item-carryover-tracker.json` | JSON skeleton conforming to the output contract schema. |
| `templates/action-item-carryover-tracker.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-action-item-carryover-tracker.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[async-standup-methodology]]
- [[burndown-diagnosis-cheatsheet]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
