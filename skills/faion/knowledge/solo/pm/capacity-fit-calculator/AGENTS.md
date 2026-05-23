---
slug: capacity-fit-calculator
tier: solo
group: pm
domain: pm
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Calculator template that validates planned sprint scope against historical velocity + known reductions before commit.
content_id: "2534aec450f5d0f3"
complexity: medium
produces: spec
est_tokens: 3800
tags: ["capacity", "pm", "solo", "sprint-planning", "velocity"]
---
# Capacity Fit Calculator

## Summary

**One-sentence:** Calculator template that validates planned sprint scope against historical velocity + known reductions before commit.

**One-paragraph:** Pins the sprint-planning input check: compute available capacity = baseline velocity × focus factor × (1 - known reductions). Output is a versioned spec; if scope > capacity, the calculator forces a cut decision before commit, not on day 5.

**Ефективно для:**

- Solo founder or PM who over-commits every sprint and runs the burndown diagnostic every Friday. Force-cuts scope at planning time using last 4 sprints of velocity data instead of optimism.

## Applies If (ALL must hold)

- Team has run ≥4 sprints with recorded velocity
- Sprint planning happens (formal or informal)
- Sprint scope is measured in points / hours / story count

## Skip If (ANY kills it)

- First 3 sprints — no baseline yet
- Solo founder doing kanban with no sprint boundary
- Tasks not estimated at all — fix estimation first

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Last 4 sprints velocity history | CSV | PM tool export |
| Known reductions for upcoming sprint (PTO, holidays, ops days) | table | team calendar |
| Proposed scope (list of stories + estimates) | table | planning meeting |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/pm/burndown-diagnosis-cheatsheet` | Peer methodology — runs when capacity fit was wrong and burndown drifts. |
| `solo/pm/audience-okr-template-indie` | Peer methodology — sprint scope must serve quarter OKRs that capacity caps. |

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
| `draft-capacity-fit-calculator` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-capacity-fit-calculator` | haiku | Schema check + threshold checks; deterministic. |
| `review-capacity-fit-calculator` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/capacity-fit-calculator.json` | JSON skeleton conforming to the output contract schema. |
| `templates/capacity-fit-calculator.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-capacity-fit-calculator.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[burndown-diagnosis-cheatsheet]]
- [[audience-okr-template-indie]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
