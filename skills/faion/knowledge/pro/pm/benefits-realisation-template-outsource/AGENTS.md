---
slug: benefits-realisation-template-outsource
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a vendor-side benefits-realisation record for an outsource engagement — deliverable vs outcome split with named owner and review cadence.
content_id: "00fe57a075debf32"
complexity: medium
produces: spec
est_tokens: 4500
tags: [benefits-realisation-template-outsource, pm, pro, spec]
---
# Benefits Realisation Template Outsource

## Summary

**One-sentence:** Generates a vendor-side benefits-realisation record for an outsource engagement — deliverable vs outcome split with named owner and review cadence.

**One-paragraph:** Benefits Realisation Template Outsource addresses the gap identified by the `role-project-manager/Project closure with benefits realisation and lessons learned (two weeks)` playbook: Generic benefits-realisation methodology is too internal-IT shaped. Outsource engagements need a vendor-side variant (deliverable vs outcome, what the client measures vs what we measure). Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned `spec` artefact carrying a named accountable owner, input citations, and a review date — downstream agents and human reviewers consume it without re-deriving the rationale.

**Ефективно для:**

- Структурований spec-артефакт, що читається людиною і парситься машиною.
- Типізовані поля з обов'язковим джерелом — жодного 'team' / 'we' як власника.
- Версіонована, ревью‑датована форма — артефакт не стає stale без сигналу.
- Контрактний валідатор blocks вихід, який не задовольняє схему.

## Applies If (ALL must hold)

- Task is an instance of `role-project-manager/Project closure with benefits realisation and lessons learned (two weeks)` OR a closely-adjacent variant in the same engagement shape.
- Operator has all artefacts named in Prerequisites available before starting.
- Output will be consumed by a downstream agent or human reviewer (not discarded after one read).
- Tier == pro or higher (gating enforced by `tier-manifest.json`).

## Skip If (ANY kills it)

- Team already maintains a working artefact for this gap — update it, do not duplicate.
- Change being decided is a greenfield prototype with no production users or paying client.
- Regulatory / compliance context overrides in-methodology guidance — defer to legal.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Recent context for the `role-project-manager/Project closure with benefits realisation and lessons learned (two weeks)` task (last 30 days) | Markdown / chat log | engagement notes |
| Write-access to the artefact store | repo / wiki / decision log | infra |
| Named accountable owner (handle / email / role) | string | engagement RACI |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[project-manager]] | Parent role skill — provides operating context for any PM artefact. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-input-citations | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for `spec` shape + valid/invalid/forbidden examples | 800 |
| `content/03-failure-modes.xml` | essential | 3+ antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate per step | 700 |
| `content/05-examples.xml` | essential | Worked end-to-end example producing a valid `spec` artefact | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping observable signals to a rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Template-fill of inputs from named sources; bounded transformation. |
| `synthesize-spec` | sonnet | Per-instance judgment over bounded inputs to fill the `spec` shape. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high (regulatory / large €). |

## Templates

| File | Purpose |
|------|---------|
| `templates/benefits-realisation-template-outsource.json` | JSON Schema (draft-07) for the Benefits Realisation Template Outsource output contract |
| `templates/benefits-realisation-template-outsource.md` | Markdown skeleton with the required fields for the Benefits Realisation Template Outsource artefact |
| `templates/benefits-realisation-template-outsource.example.json` | Worked filled-in example of a valid Benefits Realisation Template Outsource artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-benefits-realisation-template-outsource.py` | Enforce the Benefits Realisation Template Outsource output contract against the JSON Schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[project-manager]]
- [[change-request-pricing-rubric]]
- [[client-status-email-template-agency]]
- upstream playbook: `role-project-manager/Project closure with benefits realisation and lessons learned (two weeks)`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input completeness, owner named yes/no, decision materiality) to a concrete action, with each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about whether to run this methodology, route to a sibling methodology, or skip entirely.
