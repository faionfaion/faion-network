---
slug: change-control
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Formal process evaluating every proposed change to scope, schedule, cost, or quality against the approved baseline via Change Request Form, CCB review, impact analysis, and decision log.
content_id: "80621a1aaee241dc"
complexity: medium
produces: config
est_tokens: 4200
tags: [change-control, scope, ccb, governance, baseline]
---
# Change Control

## Summary

**One-sentence:** Formal process evaluating every proposed change to scope, schedule, cost, or quality against the approved baseline via Change Request Form, CCB review, impact analysis, and decision log.

**One-paragraph:** Formal process evaluating every proposed change to scope, schedule, cost, or quality against the approved baseline via Change Request Form, CCB review, impact analysis, and decision log. The methodology applies in pm-traditional contexts where the preconditions in `Applies If` hold and none of the `Skip If` triggers fire. Decision routing lives in `content/06-decision-tree.xml`; testable rules with rationale live in `content/01-core-rules.xml`; the validator at `scripts/validate-change-control.py` enforces the output contract.

**Ефективно для:**

- Fixed-price contracts where scope creep destroys margin.
- Regulated programs requiring audit trail of every change.
- Multi-vendor programs with contractually defined scope baselines.
- Capital projects with locked budgets and milestone-funded gates.

## Applies If (ALL must hold)

- A baselined scope, schedule, and cost exist.
- A Change Control Board (CCB) or equivalent decision body exists.
- Stakeholders accept formal CR turnaround time (typically 3-10 working days).

## Skip If (ANY kills it)

- Agile delivery without baselines — use backlog re-ordering instead.
- Experimental phase pre-baseline.
- Single-developer side project.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Scope baseline | Markdown/CSV | PM |
| Schedule baseline | Gantt/JSON | scheduler |
| Cost baseline | Currency total | Finance |
| CCB roster | named list | Sponsor |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[project-integration]] | integration baselines are the change reference |

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
| `draft-cr` | sonnet | Judgement: impact analysis across scope/schedule/cost. |
| `score-cr-priority` | haiku | Mechanical urgency + impact → priority. |
| `detect-drift` | haiku | Diff current vs baseline to detect un-controlled change. |

## Templates

| File | Purpose |
|------|---------|
| `templates/change-register.md` | Change register template with CR ID, requestor, decision, baseline impact |
| `templates/change-request-form.md` | Change Request Form template: trigger, impact, alternatives, recommendation |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-change-control.py` | Validate the config artefact against the schema in `02-output-contract.xml` | CI on each artefact change; pre-commit |

## Related

- [[project-integration]]
- [[communications-management]]
- [[procurement-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions, baseline presence, threshold pass/fail) to a concrete action; each leaf references a rule from `01-core-rules.xml`. Use it when in doubt about whether or how to apply this methodology to the case at hand.

