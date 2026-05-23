---
slug: contractor-audition-rubric
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a contractor audition score — technical, comms, ownership, fit, paid trial result — with explicit pass threshold and named decider.
content_id: "5f98a5011d277e36"
complexity: medium
produces: rubric
est_tokens: 3800
tags: [contractor-audition-rubric, pm, pro, rubric]
---
# Contractor Audition Rubric

## Summary

**One-sentence:** Generates a contractor audition score — technical, comms, ownership, fit, paid trial result — with explicit pass threshold and named decider.

**One-paragraph:** Contractor Audition Rubric addresses the gap identified by the `p5-micro-agency-founder/Hiring screen / contractor audition` playbook: Auditions get scored on vibes. A rubric pins each dimension to evidence and a binary pass threshold per dimension. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned `rubric` artefact carrying a named accountable owner, input citations, and a review date — downstream agents and human reviewers consume it without re-deriving the rationale.

**Ефективно для:**

- Зважений scorecard з явними ваговими коефіцієнтами та порогом pass / fail.
- Кожен вимір прив'язаний до evidence, а не до vibes — ревью‑friendly.
- Артефакт несе версію + last_reviewed; стейл flagged on read.
- Контрактний валідатор перевіряє діапазони + threshold + наявність owner.

## Applies If (ALL must hold)

- Task is an instance of `p5-micro-agency-founder/Hiring screen / contractor audition` OR a closely-adjacent variant in the same engagement shape.
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
| Recent context for the `p5-micro-agency-founder/Hiring screen / contractor audition` task (last 30 days) | Markdown / chat log | engagement notes |
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
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for `rubric` shape + valid/invalid/forbidden examples | 800 |
| `content/03-failure-modes.xml` | essential | 3+ antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate per step | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping observable signals to a rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Template-fill of inputs from named sources; bounded transformation. |
| `synthesize-rubric` | sonnet | Per-instance judgment over bounded inputs to fill the `rubric` shape. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high (regulatory / large €). |

## Templates

| File | Purpose |
|------|---------|
| `templates/contractor-audition-rubric.json` | JSON Schema (draft-07) for the Contractor Audition Rubric output contract |
| `templates/contractor-audition-rubric.md` | Markdown skeleton with the required fields for the Contractor Audition Rubric artefact |
| `templates/contractor-audition-rubric.example.json` | Worked filled-in example of a valid Contractor Audition Rubric artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-contractor-audition-rubric.py` | Enforce the Contractor Audition Rubric output contract against the JSON Schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[project-manager]]
- [[change-request-pricing-rubric]]
- [[client-status-email-template-agency]]
- upstream playbook: `p5-micro-agency-founder/Hiring screen / contractor audition`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input completeness, owner named yes/no, decision materiality) to a concrete action, with each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about whether to run this methodology, route to a sibling methodology, or skip entirely.
