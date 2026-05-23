---
slug: cost-anomaly-runbook
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a per-anomaly investigation artefact (input data, root-cause hypotheses, owner, action) for one cloud cost spike per pass.
content_id: "d91114607f91602e"
complexity: medium
produces: playbook-step
est_tokens: 4500
tags: [cost-anomaly, finops, runbook, infra]
---
# Cost Anomaly Runbook

## Summary

**One-sentence:** Produces a per-anomaly investigation artefact (input data, root-cause hypotheses, owner, action) for one cloud cost spike per pass.

**One-paragraph:** FinOps methodologies are framework-level. The repeatable per-anomaly investigation is missing. This methodology pins typed inputs (spike vector, affected service, time window, billing snapshot), bounded transformations (delta vs baseline, attribution to commit / config change / traffic), and a contract-checked output: a decision record naming root-cause hypothesis, owner, and corrective action. Downstream consumers act without re-deriving the rationale.

**Ефективно для:**

- weekly cloud cost review знаходить spike — потрібен structured investigation замість chat.
- коли FinOps-frameworks (visibility / rightsizing) є, а per-anomaly runbook відсутній.
- DevOps з write-access до billing dashboards, який повинен звітувати власнику.
- tier=pro команд із multi-cloud spend де anomalies повторюються.

## Applies If (ALL must hold)

- Weekly cloud-cost review surfaces an anomaly that needs structured investigation.
- Billing snapshot for the anomaly window is queryable from the provider.
- A named owner is accountable for the resulting decision record.
- Output will be consumed by a downstream agent or human reviewer (not discarded).

## Skip If (ANY kills it)

- Anomaly is already a known + accepted seasonal spike (e.g., end-of-month batch) — no runbook needed.
- Spike is < 5% of monthly spend AND under team's noise threshold.
- Greenfield project with no production traffic — wait for steady-state baselines.
- Provider billing API is currently unavailable — defer until data is queryable.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Billing snapshot | provider CSV / API | cloud-provider billing |
| Deployment + config-change log | git / CD tool | repo |
| Service ownership map | YAML / wiki | platform team |
| Named owner | string | engagement lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer` | parent role skill — operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules with statement + rationale + source (5+ rules, includes r1-bound-scope) | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | ~900 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom/root-cause/fix | ~1000 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate per step | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Structured extraction from billing + change-log |
| `synthesize_decision` | sonnet | Per-anomaly judgement with bounded inputs |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Cost anomaly runbook artefact skeleton |
| `templates/skeleton.json` | JSON schema for the anomaly record |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cost-anomaly-runbook.py` | Validate produced artefact against the 02-output-contract.xml schema | After subagent returns, before downstream consumer reads |

## Related

- [[finops-baseline]]
- [[cost-pr-gate-recipe]]
- [[cost-model-spreadsheet-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, owner, downstream consumer) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it before applying the Cost Anomaly Runbook methodology when in doubt about scope or fit.
