---
slug: opentelemetry-rollout-runbook
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Step-by-step rollout runbook for OTel: pilot service, sampling baseline, collector capacity, vendor cutover, decommission of legacy agents, KPI dashboards.
content_id: "437da02fb709eba1"
complexity: deep
produces: playbook-step
est_tokens: 3600
tags: [opentelemetry, otel, rollout, runbook, infra]
---
# OpenTelemetry Rollout Runbook

## Summary

**One-sentence:** Step-by-step rollout runbook for OTel: pilot service, sampling baseline, collector capacity, vendor cutover, decommission of legacy agents, KPI dashboards.

**One-paragraph:** Step-by-step rollout runbook for OTel: pilot service, sampling baseline, collector capacity, vendor cutover, decommission of legacy agents, KPI dashboards. Output is a versioned artefact a downstream agent or human reviewer can consume without re-deriving the rationale. Hard rules are pinned in `content/01-core-rules.xml`; the JSON Schema contract in `content/02-output-contract.xml` gates downstream consumption; failure modes in `content/03-failure-modes.xml` block the common antipatterns observed in real deployments.

**Ефективно для:**

- Підприємство платить вендору $50k+/міс — є реальна мотивація переходити на OTel поетапно.
- Pilot service вже інструментовано (instrumentation playbook закрито) — час масштабувати.
- Vendor contract має renewal date — без runbook ризик пропустити cost lever.
- Команда хоче KPI dashboard: cost per span, error rate, ingest volume по тижнях.

## Applies If (ALL must hold)

- Org has legacy vendor agents (Datadog, AppDynamics) AND wants to migrate to OTel
- >=5 services included in the first rollout wave
- KPI dashboards exist (trace volume, cost, error rate)
- Vendor contract cutover date is in scope (cost lever)

## Skip If (ANY kills it)

- Greenfield service — instrumentation playbook is enough, no rollout planning needed
- Org-wide cutover deferred to next quarter — defer the runbook
- Legacy agents already removed — only ongoing tuning remains

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Trigger context | Markdown / ticket / transcript | upstream task |
| Named owner | string (handle, email, role) | team roster |
| Storage location | URL / repo path | artefact store |
| Prior cycle artefact (if any) | this methodology's output | last run |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/AGENTS.md` | parent group context (vocabulary, neighbouring methodologies) |
| `solo/sdd/sdd` | SDD discipline for artefact lifecycle (status flow, owners, review) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + run-the-checklist + skip-this-methodology conclusions | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid + invalid + forbidden examples | ~800 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom / root-cause / fix | ~700 |
| `content/04-procedure.xml` | essential | step-by-step procedure (input/action/output/decision-gate) | ~700 |
| `content/06-decision-tree.xml` | essential | root-question + branches + conclusion refs to 01-core-rules | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment over bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high or evidence chain is required |

## Templates

| File | Purpose |
|------|---------|
| `templates/playbook-step.md` | working skeleton matching the `produces=playbook-step` shape |
| `templates/_smoke-test.md` | minimum-viable filled-in smoke-test fixture |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-opentelemetry-rollout-runbook.py` | enforce `02-output-contract.xml` JSON Schema | after subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/infra/`
- peer methodology: see other entries in `skills/faion/knowledge/pro/infra/`
- external: industry references cited inline in `content/01-core-rules.xml`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts at `Is the org migrating from legacy vendor agents to OTel across >=5 services with a contract cutover date?` and routes to one of the 5 conclusions referencing rules in `01-core-rules.xml` (run-the-checklist, skip-this-methodology, defer-to-upstream, escalate-to-owner, schedule-recompute). Use it when in doubt about applicability or scope.
