# Project Integration Management

## Summary

**One-sentence:** PM acts as integrator across knowledge areas via a single version-controlled integrated plan; every change triggers cross-area impact analysis; status colour follows numeric thresholds.

**One-paragraph:** The PM acts as cross-area integrator across scope, schedule, cost, quality, risk, resources, communications, procurement. One source of truth is integrated/plan.yaml; derivatives (slides, dashboards, PDFs) are generated, never hand-edited. Every change request triggers a cross-area impact memo committed alongside the CR before implementation. Status colour is derived from numeric thresholds, not PM narrative. Closure is integration's last mile.

**Ефективно для:**

- Programme with ≥2 workstreams whose decisions interact
- Initiation: drafting the project charter to bind sponsor commitment
- Change-heavy environment where every CR has cross-area impact
- Multi-team / multi-vendor delivery where local optimisation harms the whole

## Applies If (ALL must hold)

- Programs with 2+ workstreams whose decisions interact
- Initiation phase: drafting the project charter to authorise work and bind sponsor commitment
- Change-heavy environments where every CR has cross-area impact simultaneously
- Multi-team or multi-vendor delivery where local optimisation harms whole-system performance
- Project closure: final integration, lessons learned, formal acceptance

## Skip If (ANY kills it)

- Single-team, single-stream work with a stable backlog — Scrum or Kanban already integrates within the team
- Short tactical engagement under 4 weeks with no inter-area trade-offs
- Pure research / discovery phase with no committed scope

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Charter draft | Markdown | sponsor + PM |
| Subsidiary plan refs | YAML paths | scope / schedule / cost / risk owners |
| Threshold table | YAML | team consensus before status reporting starts |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[scope-management]] | Scope baseline feeds integrated plan scope reference |
| [[schedule-development]] | Schedule baseline feeds integrated plan schedule reference |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: single-source-of-truth, charter-as-code, cross-area-impact-memo, numeric-thresholds-for-status, rebaseline-only-on-cr | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the artefact + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output per step | 800 |
| `content/05-examples.xml` | essential | Full worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-charter` | opus | Cross-input judgement; sponsor-binding artefact |
| `compute-status` | haiku | Mechanical threshold comparison in script |
| `cr-impact-memo` | sonnet | Per-area delta with cited sources |

## Templates

| File | Purpose |
|------|---------|
| `templates/charter.md` | Project charter with SMART objectives, success criteria, constraints, approval block |
| `templates/status-report.md` | Weekly status report with GREEN/YELLOW/RED per knowledge area |
| `templates/integrated-plan.yaml` | Integrated plan single-source-of-truth referencing all subsidiary plans |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/integration-status.py` | Compute status colours from numeric YAML inputs via threshold ladders | Weekly pre-status-report; pre-steering |

## Related

- parent skill: `pro/pm/project-manager/`
- [[scope-management]]
- [[schedule-development]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
