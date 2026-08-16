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
| `templates/capacity-fit-calculator.md.j2` | Markdown skeleton for human-readable artefact rendering. |
| `templates/capacity-fit-calculator.md` | Markdown skeleton for human-readable artefact rendering. Generated from `templates/capacity-fit-calculator.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-capacity-fit-calculator.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[burndown-diagnosis-cheatsheet]]
- [[audience-okr-template-indie]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/capacity-fit-calculator.json`

```json
{
  "artefact_id": "capacity-fit-2026-w22",
  "version": "1.0.0",
  "last_reviewed": "2026-05-23",
  "sprint_id": "2026-W22",
  "baseline_velocity": 24,
  "focus_factor": 0.75,
  "reductions": [
    {
      "reason": "ruslan-pto-1d",
      "points": 4
    }
  ],
  "available_capacity": 14,
  "proposed_scope": 16,
  "fit_decision": "cut-required",
  "owner": "@ruslan"
}
```
