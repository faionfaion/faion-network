# On-Call Rotation Setup

## Summary

**One-sentence:** On-call rotation configuration: shift length, schedule generator, primary/secondary tiers, paging policies, compensation, fairness audit cadence.

**One-paragraph:** On-call rotation configuration: shift length, schedule generator, primary/secondary tiers, paging policies, compensation, fairness audit cadence. This methodology converts the inputs in Prerequisites into the artefact described in Output Contract, gated by the rules in 01-core-rules.xml and the decision tree in 06-decision-tree.xml.

**Ефективно для:** the kinds of tasks listed in 'Applies If' — primary use cases are teams shipping the artefact (`config`) at a medium complexity level, where the failure modes in 03-failure-modes.xml are realistic risks worth the methodology's overhead.

## Applies If (ALL must hold)

- Production service requires ≥1 engineer available 24/7 or business-hours-extended.
- Team has ≥3 engineers (smaller teams cannot rotate sustainably).
- On-call is a paid or in-comp activity at the org level.

## Skip If (ANY kills it)

- Single-engineer service with passive on-call only (best-effort).
- All issues are auto-remediable — on-call rotation overkill.
- Service is internal-only with no production SLA.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Headcount + skill matrix | Spreadsheet | team lead |
| Paging platform | PagerDuty / OpsGenie / Splunk | infra |
| Compensation policy | Markdown | HR |
| Coverage window | calendar / SLA doc | ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/infra/oncall-handoff-protocol` | Handoff happens between shifts defined here. |
| `pro/comms/hr-recruiter/compensation-policy-template` | Compensation interacts with on-call pay. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3-5 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | medium | 4-6 step procedure with input/action/output per step | ~900 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `schedule_generate` | haiku | Deterministic round-robin / pattern fill. |
| `fairness_audit` | sonnet | Compute per-engineer load across N months. |
| `compensation_policy_compose` | opus | Cross-input HR + legal + ops synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rotation-config.yaml` | Paging-platform rotation config. |
| `templates/fairness-report.md` | Per-engineer load report template. |
| `templates/compensation-policy.md` | On-call comp + time-off-in-lieu policy. |
| `templates/_smoke-test.yaml` | Minimum-viable filled-in example (smoke test). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-on-call-rotation-setup.py` | Validate methodology output against `02-output-contract.xml` schema. | Pre-commit and CI before merge. |

## Related

- parent skill: `geek/infra/`
- `[[oncall-handoff-protocol]]`
- `[[compensation-policy-template]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether on-call-rotation-setup applies: root question — "Does the service require 24/7 coverage AND team has ≥3 engineers?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip-this-methodology` conclusion when it does not.
