# Burndown Diagnosis Cheatsheet

## Summary

**One-sentence:** One-page cheatsheet for diagnosing why a burndown chart is off-track: scope creep / capacity loss / blocker stack / estimate drift.

**One-paragraph:** Pins a 4-cause diagnostic flow for off-track burndowns: scope creep, capacity loss, blocker stack, estimate drift. Output is a versioned spec naming the cause, evidence, and remediation — the founder runs it in <15 min mid-sprint instead of staring at the chart.

**Ефективно для:**

- Solo founder or PM watching a sprint burndown go flat at day 5 of 10 with no idea why. 15-min diagnostic that names the cause and remediation instead of just 'we're behind'.

## Applies If (ALL must hold)

- Active sprint with ≥3 days remaining
- Burndown chart available (Linear / Jira / GitHub Projects / spreadsheet)
- Actual line is ≥20% above ideal line at mid-sprint

## Skip If (ANY kills it)

- Sprint not started (no data)
- Sprint within last 1 day — restart sprint planning instead
- Single-task sprint — diagnostic overkill

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Current sprint scope (list of stories + estimates) | table | sprint planning |
| Daily burndown data points (ideal vs actual) | CSV | PM tool export |
| Sprint goal statement | doc | sprint kickoff |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/pm/audience-okr-template-indie` | Peer methodology — sprint feeds the quarter OKRs that burndown drift threatens. |
| `solo/pm/capacity-fit-calculator` | Peer methodology — capacity-loss diagnosis routes here for re-planning. |

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
| `draft-burndown-diagnosis-cheatsheet` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-burndown-diagnosis-cheatsheet` | haiku | Schema check + threshold checks; deterministic. |
| `review-burndown-diagnosis-cheatsheet` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/burndown-diagnosis-cheatsheet.json` | JSON skeleton conforming to the output contract schema. |
| `templates/burndown-diagnosis-cheatsheet.md` | Markdown skeleton for human-readable artefact rendering. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-burndown-diagnosis-cheatsheet.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[capacity-fit-calculator]]
- [[action-item-carryover-tracker]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/burndown-diagnosis-cheatsheet.json`

```json
{
  "artefact_id": "burndown-diag-sprint-2026-w20",
  "version": "1.0.0",
  "last_reviewed": "2026-05-23",
  "sprint_id": "2026-W20",
  "diagnosis_date": "2026-05-22",
  "drift_pct": 35,
  "diagnosed_causes": [
    {
      "cause": "scope-creep",
      "evidence": [
        "STORY-117 added day 3",
        "STORY-118 added day 4"
      ]
    },
    {
      "cause": "blocker-stack",
      "evidence": [
        "BLOCK-7 stale 4 days waiting on design"
      ]
    }
  ],
  "remediations": [
    {
      "action": "Move STORY-117/118 to next sprint",
      "owner": "@ruslan",
      "due": "2026-05-23"
    },
    {
      "action": "Escalate BLOCK-7 to async designer; set 24h ETA",
      "owner": "@ruslan",
      "due": "2026-05-23"
    }
  ],
  "owner": "@ruslan"
}
```
