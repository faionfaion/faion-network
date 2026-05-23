---
slug: on-call-shift-retro-cadence
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Per-shift retrospective cadence + report: what paged, what was noise, what should auto-remediate, what alerts to delete. Feeds back into runbook + alert tuning.
content_id: "fa7b0151f8aa77f1"
complexity: medium
produces: report
est_tokens: 4300
tags: [on-call, retro, cadence, alerts, infra]
---
# On-Call Shift Retro Cadence

## Summary

**One-sentence:** Per-shift retrospective cadence + report: what paged, what was noise, what should auto-remediate, what alerts to delete. Feeds back into runbook + alert tuning.

**One-paragraph:** Per-shift retrospective cadence + report: what paged, what was noise, what should auto-remediate, what alerts to delete. Feeds back into runbook + alert tuning. Output is a versioned artefact a downstream agent or human reviewer can consume without re-deriving the rationale. Hard rules are pinned in `content/01-core-rules.xml`; the JSON Schema contract in `content/02-output-contract.xml` gates downstream consumption; failure modes in `content/03-failure-modes.xml` block the common antipatterns observed in real deployments.

**Ефективно для:**

- Шифт мав 5+ pages з 4 false positives — без retro alerts залишаться шумом.
- Команда має повноваження видаляти / тюнити alerts — інакше retro = звіт у нікуди.
- Backlog 'tuning' / 'auto-remediate' існує і реально працюється.
- Reliability owner хоче метрику noise ratio і trend over weeks.

## Applies If (ALL must hold)

- Shift had >=1 page (real or false)
- Team has authority to tune alerts and add auto-remediation
- Retro is consumed by next shift's on-call lead + reliability owner
- Output feeds an alert-tuning backlog (jira / linear / github issues)

## Skip If (ANY kills it)

- Shift was zero-page silence — retro is one line, skip the template
- Team already does a per-incident postmortem covering the same ground
- Cadence not yet established — start with handoff template first

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
| `content/05-examples.xml` | essential | one worked end-to-end example with inputs and final artefact | ~700 |
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
| `templates/report.md` | working skeleton matching the `produces=report` shape |
| `templates/_smoke-test.md` | minimum-viable filled-in smoke-test fixture |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-on-call-shift-retro-cadence.py` | enforce `02-output-contract.xml` JSON Schema | after subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/infra/`
- peer methodology: see other entries in `skills/faion/knowledge/pro/infra/`
- external: industry references cited inline in `content/01-core-rules.xml`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts at `Did the shift have >=1 page + does the team have authority to tune alerts?` and routes to one of the 5 conclusions referencing rules in `01-core-rules.xml` (run-the-checklist, skip-this-methodology, defer-to-upstream, escalate-to-owner, schedule-recompute). Use it when in doubt about applicability or scope.
