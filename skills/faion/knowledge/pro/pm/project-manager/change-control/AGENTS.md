---
slug: change-control
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Route every change request through a formal log → impact analysis → tiered decision → baseline update cycle, with named approvers per change-size tier.
content_id: "9bc1a4d0e2f5b6c7"
complexity: medium
produces: spec
est_tokens: 4300
tags: [change-control, governance, scope, approval, baseline]
---
# Change Control

## Summary

**One-sentence:** Route every change request through a formal log → impact analysis → tiered decision → baseline update cycle, with named approvers per change-size tier.

**One-paragraph:** Route every change request through a formal log → impact analysis → tiered decision → baseline update cycle, with named approvers per change-size tier.

**Ефективно для:**

- Проектів із зафіксованим scope-baseline, де scope-creep тематично знищує margin.
- Регульованих програм, де audit trail обов'язковий.
- Програм >1M USD з кількома стейкхолдерами.
- PMO з декількома одночасними проектами і єдиним governance.

## Applies If (ALL must hold)

- Project has a written scope/schedule/cost baseline.
- Stakeholders > 3 with conflicting change desires.
- Compliance regime requires CR audit trail.
- Project value > 1M or fixed-price contract in force.

## Skip If (ANY kills it)

- Agile project with empty/rolling baseline.
- Solo solopreneur project — overhead exceeds benefit.
- Internal R&D with deliberately fluid scope.
- Project < 2 weeks duration.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Scope brief | Markdown | engagement intake |
| Stakeholder roster | table | PM |
| Historical reference data | csv / log | PMO data warehouse |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[cost-estimation]] | Cost baseline that change-impact analysis compares against. |
| [[communications-management]] | Comms plan that routes CR approvals. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + `skip-this-methodology` | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden | 850 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 750 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/05-examples.xml` | essential | one worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Apply/skip routing on observable signals | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `cr-log-author` | haiku | Append CR row to register. |
| `impact-analysis` | sonnet | Estimate cost/schedule/scope impact. |
| `tier-router` | sonnet | Route to correct approver tier. |
| `baseline-update` | haiku | Re-baseline once CR approved. |

## Templates

| File | Purpose |
|------|---------|
| `templates/change-request.md` | CR document: requester, description, justification, impact, attachments. |
| `templates/change-register.md` | Register row: id, status, tier, decision, approver, baseline-version. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-change-control.py` | Validate the output artefact against the schema | Pre-commit on every artefact change |

## Related

- [[cost-estimation]]
- [[communications-management]]
- [[lessons-learned]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observables (baseline_frozen, value_band_USD, compliance_required) to apply / fall-back / skip. Each leaf references a rule from `01-core-rules.xml`.
