---
slug: resource-management
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Plan to 70% utilisation (not 100%), map skills to tasks from YAML roster in git, level resource load via critical-path analysis, track allocations weekly against actuals.
content_id: "c287bf8e68309063"
complexity: medium
produces: config
est_tokens: 4200
tags: [resource-management, capacity-planning, pmbok, utilization, skill-matrix]
---
# Resource Management

## Summary

**One-sentence:** Plan to 70% utilisation (not 100%), map skills to tasks from YAML roster in git, level resource load via critical-path analysis, track allocations weekly against actuals.

**One-paragraph:** Plan to 70% utilisation (not 100%), map skills to tasks from YAML roster in git, level resource load via critical-path analysis, track allocations weekly against actuals. The methodology applies in pm-traditional contexts where the preconditions in `Applies If` hold and none of the `Skip If` triggers fire. Decision routing lives in `content/06-decision-tree.xml`; testable rules with rationale live in `content/01-core-rules.xml`; the validator at `scripts/validate-resource-management.py` enforces the output contract.

**Ефективно для:**

- Programs with shared resources across multiple projects.
- PMO capacity planning across teams.
- Skill-matrix-based assignment when work demands specific competencies.
- Detection of over-allocation hot spots before they slip schedules.

## Applies If (ALL must hold)

- Roster (people × skills × availability) is available.
- Tasks have effort estimates + critical-path knowledge.
- Weekly allocation tracking is feasible.

## Skip If (ANY kills it)

- Single dedicated team with no shared resources.
- Roster not maintained — fix data quality first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Resource roster | YAML (person × skills × availability) | PMO / HR |
| Task effort estimates | hours per task | PM |
| Critical path | list of tasks | scheduler |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[cost-estimation]] | effort estimates feed resource demand |
| [[team-development]] | skills matrix is the per-team feed |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (incl. skip rule) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom/root-cause/fix triplets | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `compute-utilisation` | haiku | Mechanical: hours assigned / hours available. |
| `level-load` | sonnet | Judgement: which task to defer to relieve over-allocation. |
| `flag-skill-gaps` | haiku | Mechanical: task requires skill X, no person has X. |

## Templates

| File | Purpose |
|------|---------|
| `templates/capacity-check.py` | Capacity check: roster + tasks → per-person utilisation + over-allocation flags |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-resource-management.py` | Validate the config artefact against the schema in `02-output-contract.xml` | CI on each artefact change; pre-commit |

## Related

- [[cost-estimation]]
- [[team-development]]
- [[scrum-ceremonies]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions, baseline presence, threshold pass/fail) to a concrete action; each leaf references a rule from `01-core-rules.xml`. Use it when in doubt about whether or how to apply this methodology to the case at hand.

