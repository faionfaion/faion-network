# RACI Matrix

## Summary

**One-sentence:** Assign exactly one Accountable per task plus ≥1 Responsible; cap Consulted at 3-4 per task; walk the matrix cell-by-cell in kickoff with all roles present.

**One-paragraph:** Assign one of four roles — Responsible (does the work), Accountable (single decision owner), Consulted (provides input), Informed (notified after) — to each role for each task. Rules: exactly one Accountable per task, ≥1 Responsible, Consulted ≤4 per task, walk the matrix cell-by-cell in the kickoff meeting with all roles present. Store as CSV in source control; agents emit unified diffs on updates, never full rewrites. Violations are flagged for the human Accountable, never silently resolved.

**Ефективно для:**

- Project kickoff with multiple roles + 'who decides?' friction
- Cross-team features (BE + FE + data + ops) with ambiguous SDD task ownership
- Vendor / contractor engagements: client-owns vs contractor-delivers split
- Audit / compliance (SOC2, ISO 27001) requiring named Accountable per control

## Applies If (ALL must hold)

- New project kickoff with multiple roles and recurring 'who decides?' friction
- Cross-team features where SDD task ownership is ambiguous
- Vendor / contractor engagements: clarify what client owns vs what contractor delivers
- Audit / compliance projects (SOC2, ISO 27001) requiring a named Accountable per control
- Solopreneur engagement with designer, developer, VA mix

## Skip If (ANY kills it)

- One-person solo task with no external stakeholders
- Pure agile teams with collective code ownership and one PO — flattens to PO=A everywhere
- Highly emergent work where roles shift weekly — matrix decays faster than it is updated

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Task list | CSV | WBS work packages or deliverables |
| Role list | list of role titles | team roster (titles, not names) |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[scope-management]] | WBS work packages provide the task rows |
| [[stakeholder-register]] | Role titles flow from stakeholder analysis |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: exactly-one-accountable, at-least-one-responsible, consulted-cap-4, walk-in-kickoff, role-titles-not-names | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the artefact + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output per step | 800 |
| `content/06-decision-tree.xml` | essential | Decision tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-matrix` | sonnet | Initial fill with hard cap C≤4 enforced in prompt |
| `validate-violations` | haiku | Mechanical rule check via raci-validate.py |
| `diff-updates` | haiku | Unified diff emission, no full rewrite |

## Templates

| File | Purpose |
|------|---------|
| `templates/raci-matrix.md` | Blank RACI grid template with role columns and task rows |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/raci-validate.py` | CSV validator checking all four rules with per-violation error output | Pre-merge on matrix changes; CI |

## Related

- parent skill: `pro/pm/project-manager/`
- [[scope-management]]
- [[stakeholder-register]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
