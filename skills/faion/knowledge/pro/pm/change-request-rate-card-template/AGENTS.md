---
slug: change-request-rate-card-template
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a versioned rate-card spec covering role tiers, blended rates, rush multipliers and travel passthrough for use on every change request.
content_id: "76db2ae64dcdb3b6"
complexity: light
produces: spec
est_tokens: 3800
tags: [change-request-rate-card-template, pm, pro, spec]
---
# Change Request Rate Card Template

## Summary

**One-sentence:** Generates a versioned rate-card spec covering role tiers, blended rates, rush multipliers and travel passthrough for use on every change request.

**One-paragraph:** Change Request Rate Card Template addresses the gap identified by the `p4-outsource-specialist/T&M to fixed-price contract conversion (6 weeks)` playbook: Without a published rate card, every CR negotiation restarts from zero. A template + per-engagement override keeps pricing fast and defensible. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned `spec` artefact carrying a named accountable owner, input citations, and a review date — downstream agents and human reviewers consume it without re-deriving the rationale.

**Ефективно для:**

- Структурований spec-артефакт, що читається людиною і парситься машиною.
- Типізовані поля з обов'язковим джерелом — жодного 'team' / 'we' як власника.
- Версіонована, ревью‑датована форма — артефакт не стає stale без сигналу.
- Контрактний валідатор blocks вихід, який не задовольняє схему.

## Applies If (ALL must hold)

- Task is an instance of `p4-outsource-specialist/T&M to fixed-price contract conversion (6 weeks)` OR a closely-adjacent variant in the same engagement shape.
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
| Recent context for the `p4-outsource-specialist/T&M to fixed-price contract conversion (6 weeks)` task (last 30 days) | Markdown / chat log | engagement notes |
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
| `templates/change-request-rate-card-template.json` | JSON Schema (draft-07) for the Change Request Rate Card Template output contract |
| `templates/change-request-rate-card-template.md` | Markdown skeleton with the required fields for the Change Request Rate Card Template artefact |
| `templates/change-request-rate-card-template.example.json` | Worked filled-in example of a valid Change Request Rate Card Template artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-change-request-rate-card-template.py` | Enforce the Change Request Rate Card Template output contract against the JSON Schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[project-manager]]
- [[change-request-pricing-rubric]]
- [[client-status-email-template-agency]]
- upstream playbook: `p4-outsource-specialist/T&M to fixed-price contract conversion (6 weeks)`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input completeness, owner named yes/no, decision materiality) to a concrete action, with each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about whether to run this methodology, route to a sibling methodology, or skip entirely.
