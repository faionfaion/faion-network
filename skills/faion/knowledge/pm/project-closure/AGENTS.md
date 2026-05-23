# Project Closure

## Summary

**One-sentence:** Formal 7-step process to end a project: signed acceptance, closed contracts, lessons learned, archived docs, final report, operations handover, team recognition.

**One-paragraph:** Formal 7-step process to end a project with: signed deliverable acceptance, financial/resource/contract closure (sequenced after handover), lessons-learned before the team disperses, structured archive, final report, operations handover, team recognition. Closure applies equally to normal, cancelled, and phase-end projects. Every checklist item is a record with status, owner, and evidence link — not a checkbox the agent self-certifies.

**Ефективно для:**

- Project objectives met and final deliverables accepted
- Project cancelled mid-flight — close formally to recover value
- Phase-end of a multi-phase programme before next-phase funding
- Absorption of a legacy project into BAU operations

## Applies If (ALL must hold)

- Project objectives met and final deliverables accepted (normal closure)
- Project cancelled mid-flight — still close formally to recover value, release resources, capture lessons
- Phase-end of a multi-phase programme before the next phase receives funding
- Agency engagement final invoice and warranty handover
- Absorption of a legacy project into BAU operations

## Skip If (ANY kills it)

- Project still has open scope, unresolved issues, or unsigned acceptance — resolve those first
- Operational or run-rate work with no defined endpoint — use service transition documents instead
- Long-tail support work after handover — that is operations, not project closure

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Deliverable list | YAML | scope baseline |
| Acceptance criteria | Markdown | scope baseline (locked before closure starts) |
| Open contracts/POs | CSV | finance / procurement |
| Access list | YAML | infra / IAM team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[scope-management]] | Acceptance criteria must be observable and agreed before closure starts |
| [[project-integration]] | Closure is integration's last mile |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: signed-acceptance-required, acceptance-criteria-precede-closure, lessons-before-dispersal, staged-decommission, access-revocation-after-handover | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the artefact + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output per step | 800 |
| `content/05-examples.xml` | essential | Full worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-final-report` | sonnet | Synthesises status, deliverables, lessons; bounded by inputs |
| `audit-checklist` | haiku | Mechanical evidence-link verification per item |
| `facilitate-lessons-learned` | opus | Cross-input judgement; surfaces root causes |

## Templates

| File | Purpose |
|------|---------|
| `templates/closure-checklist.md` | Complete closure checklist grouped by category |
| `templates/deliverable-acceptance.md` | Acceptance form with criteria table and signature block |
| `templates/handover.md` | Operations handover: system overview, docs, support contacts, known issues |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/closure-audit.py` | Validates closure_checklist.yaml completeness and evidence links | Pre-sponsor-signoff; CI on closure packet |

## Related

- parent skill: `pro/pm/project-manager/`
- [[scope-management]]
- [[project-integration]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
