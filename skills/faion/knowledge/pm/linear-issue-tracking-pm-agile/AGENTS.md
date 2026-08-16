# Linear Issue Tracking (PM Agile)

## Summary

**One-sentence:** Solo / small-team Linear setup: workspace, cycle policy, issue states, label taxonomy, Slack/GitHub linkages, automation hygiene.

**One-paragraph:** Pins the Linear baseline for solo founders + small teams: one workspace, weekly cycles, canonical state set, ≤15 labels, GitHub + Slack integrations on. Output is a versioned spec covering setup + governance + agent-integration limits.

**Ефективно для:**

- Solo founder or 2-10-person team adopting Linear who wants to skip the rewrite-in-month-3 phase. One spec covering workspace shape, cycle policy, label taxonomy, integrations.

## Applies If (ALL must hold)

- Adopting Linear OR auditing existing Linear workspace
- Team size 1-10 (small enough for one workspace)
- Issues estimated in story points OR T-shirt sizes

## Skip If (ANY kills it)

- Already use Jira / GitHub Projects exclusively and not migrating
- Team size >25 — Linear architecture differs from enterprise
- Issues are not estimated AND not planning to start

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Team roster + roles | table | people doc |
| Existing repos / Slack channels to integrate | list | stack inventory |
| Cycle length decision (1w / 2w) | doc | team agreement |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/pm/capacity-fit-calculator` | Peer methodology — capacity computation reads Linear estimates. |
| `solo/pm/burndown-diagnosis-cheatsheet` | Peer methodology — burndown chart sourced from Linear cycle data. |

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
| `templates/linear-issue-tracking.md.j2` | Markdown skeleton for human-readable artefact rendering. |
| `templates/linear-issue-tracking.md` | Markdown skeleton for human-readable artefact rendering. Generated from `templates/linear-issue-tracking.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/issue-bug.md.j2` | Linear bug issue template — environment, repro steps, severity. |
| `templates/issue-bug.md` | Linear bug issue template — environment, repro steps, severity. Generated from `templates/issue-bug.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/issue-feature.md.j2` | Linear feature issue template — problem, solution, user stories, acceptance criteria, metrics. |
| `templates/issue-feature.md` | Linear feature issue template — problem, solution, user stories, acceptance criteria, metrics. Generated from `templates/issue-feature.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[capacity-fit-calculator]]
- [[github-projects]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/linear-issue-tracking.json`

```json
{
  "artefact_id": "linear-setup-2026-q2",
  "version": "1.0.0",
  "last_reviewed": "2026-05-23",
  "workspace_url": "https://linear.app/faion",
  "cycle_length_days": 14,
  "states": [
    "Backlog",
    "Todo",
    "In Progress",
    "In Review",
    "Done",
    "Cancelled"
  ],
  "labels": [
    "bug",
    "feat",
    "chore",
    "spike",
    "docs",
    "infra"
  ],
  "integrations": {
    "github": true,
    "slack": true,
    "calendar": true
  },
  "estimation_method": "points",
  "owner": "@ruslan"
}
```
