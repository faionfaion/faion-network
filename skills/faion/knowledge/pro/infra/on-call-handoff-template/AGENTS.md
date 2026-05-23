---
slug: on-call-handoff-template
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Per-shift on-call handoff report template: open incidents, watch-list alerts, paged-but-resolved log, planned maintenance, hand-over notes per service.
content_id: "4aecc055c3acf451"
complexity: medium
produces: report
est_tokens: 4300
tags: [on-call, handoff, report, incidents, infra]
---
# On-Call Handoff Template

## Summary

**One-sentence:** Per-shift on-call handoff report template: open incidents, watch-list alerts, paged-but-resolved log, planned maintenance, hand-over notes per service.

**One-paragraph:** Per-shift on-call handoff report template: open incidents, watch-list alerts, paged-but-resolved log, planned maintenance, hand-over notes per service. Output is a versioned artefact a downstream agent or human reviewer can consume without re-deriving the rationale. Hard rules are pinned in `content/01-core-rules.xml`; the JSON Schema contract in `content/02-output-contract.xml` gates downstream consumption; failure modes in `content/03-failure-modes.xml` block the common antipatterns observed in real deployments.

**Ефективно для:**

- Зміни рот ротуються щотижня — без шаблону передається тільки 'я нічого не запам'ятав'.
- PagerDuty/OpsGenie містять timestamps, але не контекст 'я бачив що це падає кожну ніч'.
- Watch-list alerts (не paged, але цікаво) живуть у голові outgoing engineer — треба зафіксувати.
- Команда планує постmortem — без структурованого handoff контекст втрачається.

## Applies If (ALL must hold)

- On-call rotation has >=2 engineers, with shift boundary (e.g. weekly)
- Incident system does not capture 'context' (only timestamps + status)
- Outgoing engineer needs to transfer mental state (watch-list, unresolved noise)
- Postmortem culture exists and handoff feeds into it

## Skip If (ANY kills it)

- Team is single on-call engineer with no rotation — handoff is no-op
- All incidents are already in a system of record (PagerDuty, OpsGenie) with structured fields
- Handoff is done verbally in standup and is sufficient (low-stakes service)

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
| `scripts/validate-on-call-handoff-template.py` | enforce `02-output-contract.xml` JSON Schema | after subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/infra/`
- peer methodology: see other entries in `skills/faion/knowledge/pro/infra/`
- external: industry references cited inline in `content/01-core-rules.xml`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts at `Does the rotation have >=2 engineers + shift boundary + need to transfer non-paging context?` and routes to one of the 5 conclusions referencing rules in `01-core-rules.xml` (run-the-checklist, skip-this-methodology, defer-to-upstream, escalate-to-owner, schedule-recompute). Use it when in doubt about applicability or scope.
