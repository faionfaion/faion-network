# Linear Issue Tracking (Project Manager)

## Summary

**One-sentence:** PM-facing Linear playbook: triage cadence, cycle ceremonies, label hygiene, reporting templates — for PMs who run Linear day-to-day.

**One-paragraph:** Pins the PM-level operating discipline for an existing Linear workspace: triage cadence, cycle ceremonies (planning + check-in + retro), label hygiene policy, weekly status template. Sister methodology to `pm-agile/linear-issue-tracking` (which covers setup); this covers operations.

**Ефективно для:**

- PM (solo or in a 2-10 team) inheriting or running a Linear workspace day-to-day. Stops the slow drift to label sprawl + missed triage by pinning the ceremonies.

## Applies If (ALL must hold)

- Linear workspace already exists (or being adopted alongside pm-agile/linear-issue-tracking)
- PM (or founder acting as PM) running ≥1 team in Linear
- Cycle cadence agreed (1w / 2w)

## Skip If (ANY kills it)

- No Linear workspace and not adopting
- Engineering team self-organises without a PM role
- Workspace size >50 active members (different playbook)

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Existing Linear workspace + admin access | config | Linear admin |
| Cycle cadence + start day documented | doc | team agreement |
| Current label taxonomy + state set | list | Linear export |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/pm/pm-agile/linear-issue-tracking` | Parent setup methodology — workspace + label + state baseline. |
| `solo/pm/burndown-diagnosis-cheatsheet` | Peer methodology — runs from Linear cycle data when drift is detected. |

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
| `draft-linear-issue-tracking` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-linear-issue-tracking` | haiku | Schema check + threshold checks; deterministic. |
| `review-linear-issue-tracking` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/linear-issue-tracking.json` | JSON skeleton conforming to the output contract schema. |
| `templates/linear-issue-tracking.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-linear-issue-tracking.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[linear-issue-tracking__pm-agile]]
- [[burndown-diagnosis-cheatsheet]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
