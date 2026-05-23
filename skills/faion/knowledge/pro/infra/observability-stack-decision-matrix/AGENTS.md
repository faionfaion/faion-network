---
slug: observability-stack-decision-matrix
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Decision-record matrix for choosing observability stack (Prometheus+Loki+Tempo vs Datadog vs New Relic vs Grafana Cloud) based on team size, budget, compliance, vendor-lock tolerance.
content_id: "2a8a7a82784a5c19"
complexity: medium
produces: decision-record
est_tokens: 3600
tags: [observability, decision-matrix, prometheus, datadog, infra]
---
# Observability Stack Decision Matrix

## Summary

**One-sentence:** Decision-record matrix for choosing observability stack (Prometheus+Loki+Tempo vs Datadog vs New Relic vs Grafana Cloud) based on team size, budget, compliance, vendor-lock tolerance.

**One-paragraph:** Decision-record matrix for choosing observability stack (Prometheus+Loki+Tempo vs Datadog vs New Relic vs Grafana Cloud) based on team size, budget, compliance, vendor-lock tolerance. Output is a versioned artefact a downstream agent or human reviewer can consume without re-deriving the rationale. Hard rules are pinned in `content/01-core-rules.xml`; the JSON Schema contract in `content/02-output-contract.xml` gates downstream consumption; failure modes in `content/03-failure-modes.xml` block the common antipatterns observed in real deployments.

**Ефективно для:**

- Команда зараз обирає observability stack — без матриці пройде 'ляписова' оцінка.
- Бюджет $500-$5k/міс — є реальна різниця між self-hosted і vendor, треба зважити.
- Compliance (EU data residency, HIPAA) урізає список вендорів — треба зафіксувати причини.
- Майбутній audit або новий tech lead захочуть знати чому саме цей stack.

## Applies If (ALL must hold)

- Team is greenfield or mid-flight migration choosing an observability stack
- Budget for observability is >=$500/month
- Compliance / data-residency constraints exist (EU, regulated industry)
- Decision needs to be defensible to a future audit or new lead

## Skip If (ANY kills it)

- Stack already chosen and locked-in for >=2 years — no decision to make
- Free-tier hobby project — Prometheus + Grafana free is the default, no matrix needed
- Team has zero ops capacity — managed SaaS is the only option, skip the matrix

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
| `templates/decision-record.md` | working skeleton matching the `produces=decision-record` shape |
| `templates/_smoke-test.md` | minimum-viable filled-in smoke-test fixture |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-observability-stack-decision-matrix.py` | enforce `02-output-contract.xml` JSON Schema | after subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/infra/`
- peer methodology: see other entries in `skills/faion/knowledge/pro/infra/`
- external: industry references cited inline in `content/01-core-rules.xml`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts at `Is the team actively choosing between >=2 observability stacks with a budget >=$500/mo?` and routes to one of the 5 conclusions referencing rules in `01-core-rules.xml` (run-the-checklist, skip-this-methodology, defer-to-upstream, escalate-to-owner, schedule-recompute). Use it when in doubt about applicability or scope.
