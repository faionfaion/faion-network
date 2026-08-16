# Backlog Grooming and Roadmapping

## Summary

**One-sentence:** Maintain a prioritised backlog and a 1-3-12 month roadmap by running a weekly grooming pass that decomposes, scores, and re-orders work items against the current product theme.

**One-paragraph:** Backlogs without weekly grooming silt up: stale tickets, missing acceptance criteria, hidden dependencies. This methodology pins a weekly cadence: every ticket is sized, scored (RICE or similar), tagged with its theme, and either promoted into the 1-month plan, parked in the 3-month roadmap, or culled. The roadmap stays a 1-3-12 view aligned to outcomes, not features; engineering picks from the top of the 1-month band.

**Ефективно для:**

- Solo founder running a single-product backlog who needs a weekly ritual to prevent drift.
- Small team where the PM and engineers share one prioritisation pass.
- Teams introducing OKRs that need a backlog→OKR mapping.
- Pre-launch projects that must trade scope for date every week.

## Applies If (ALL must hold)

- A backlog tool (issue tracker, board) is already in place.
- At least one weekly time slot exists for grooming.
- Product theme or OKR for the current quarter is defined.
- ≥1 owner can sign off prioritisation outcomes.

## Skip If (ANY kills it)

- Discovery phase where requirements are still unknown — no backlog yet.
- Pure run-the-business work with no roadmap decision required.
- Single-task project where prioritisation is trivial.
- Team already runs Scrum-style refinement that covers this scope — use Scrum methodology instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Backlog dump | issue tracker export | Linear / Jira / GitHub Issues |
| Current quarter theme / OKR | document | product-planning output |
| Sizing scale | rubric | Team doc |
| Roadmap horizon list | 1-3-12 outline | Previous grooming pass |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd-planning/spec-structure` | New backlog items reference specs once promoted. |
| `solo/sdd/sdd-planning/impl-plan-task-format` | Promoted items decompose into TASK files. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `score-items` | haiku | Apply RICE / WSJF formulas — deterministic numerics. |
| `draft-roadmap-shift` | sonnet | Re-balance 1-3-12 horizons with judgement. |
| `theme-review` | opus | Quarterly synthesis across multiple OKRs. |

## Templates

| File | Purpose |
|------|---------|
| `templates/backlog-grooming-roadmapping.json` | JSON skeleton conforming to the output contract schema. |
| `templates/backlog-grooming-roadmapping.md.j2` | Markdown skeleton for human-readable artefact rendering. |
| `templates/backlog-grooming-roadmapping.md` | Markdown skeleton for human-readable artefact rendering. Generated from `templates/backlog-grooming-roadmapping.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/backlog-item.md.j2` | Single prioritised backlog item with RICE score, MoSCoW classification, dependencies, and next steps. |
| `templates/backlog-item.md` | Single prioritised backlog item with RICE score, MoSCoW classification, dependencies, and next steps. Generated from `templates/backlog-item.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/grooming-session.md.j2` | Weekly grooming session log — new ideas reviewed, priority changes, items refined/archived, next sprint candidates, action items. |
| `templates/grooming-session.md` | Weekly grooming session log — new ideas reviewed, priority changes, items refined/archived, next sprint candidates, action items. Generated from `templates/grooming-session.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/roadmap.md.j2` | 1-3-12 month product roadmap — Now/Next/Later milestones, not-planned items, dependencies, change log. |
| `templates/roadmap.md` | 1-3-12 month product roadmap — Now/Next/Later milestones, not-planned items, dependencies, change log. Generated from `templates/roadmap.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

- [[impl-plan-task-format]]
- [[backlog-grooming-roadmapping]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/backlog-grooming-roadmapping.json`

```json
{
  "artefact_id": "backlog-grooming-roadmapping-example",
  "version": "1.0.0",
  "last_reviewed": "2026-05-23",
  "grooming_date": "2026-05-23",
  "items_total": 1,
  "items_promoted": 1,
  "items_culled": 1,
  "horizons": {
    "key": "value"
  },
  "theme_orphans": [
    "item-1",
    "item-2",
    "item-3"
  ],
  "owner": "@solo-founder"
}
```
