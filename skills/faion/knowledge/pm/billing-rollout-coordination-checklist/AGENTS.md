# Billing Rollout Coordination Checklist

## Summary

**One-sentence:** Generates a pre-flight checklist for shipping a billing/pricing change — comms, ops, support, legal, finance gates with named owners.

**One-paragraph:** Billing Rollout Coordination Checklist addresses the gap identified by the `role-product-manager/Pricing experiment, hypothesis to result` playbook: Pricing experiments require coordinated change in payment provider, comms, support scripts, and finance reconciliation. Without a coordination checklist one of these always lags. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned `checklist` artefact carrying a named accountable owner, input citations, and a review date — downstream agents and human reviewers consume it without re-deriving the rationale.

**Ефективно для:**

- Бінарний checklist, де кожен пункт має owner і `done_by` дату.
- Sign-off field — артефакт неможливо позначити complete без named approver.
- Версіонована форма + last_reviewed; redo at next cycle.
- Контрактний валідатор перевіряє, що всі обов'язкові пункти заповнені.

## Applies If (ALL must hold)

- Task is an instance of `role-product-manager/Pricing experiment, hypothesis to result` OR a closely-adjacent variant in the same engagement shape.
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
| Recent context for the `role-product-manager/Pricing experiment, hypothesis to result` task (last 30 days) | Markdown / chat log | engagement notes |
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
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for `checklist` shape + valid/invalid/forbidden examples | 800 |
| `content/03-failure-modes.xml` | essential | 3+ antipatterns with symptom / root-cause / fix | 800 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping observable signals to a rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Template-fill of inputs from named sources; bounded transformation. |
| `synthesize-checklist` | sonnet | Per-instance judgment over bounded inputs to fill the `checklist` shape. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high (regulatory / large €). |

## Templates

| File | Purpose |
|------|---------|
| `templates/billing-rollout-coordination-checklist.json` | JSON Schema (draft-07) for the Billing Rollout Coordination Checklist output contract |
| `templates/billing-rollout-coordination-checklist.md` | Markdown skeleton with the required fields for the Billing Rollout Coordination Checklist artefact |
| `templates/billing-rollout-coordination-checklist.example.json` | Worked filled-in example of a valid Billing Rollout Coordination Checklist artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-billing-rollout-coordination-checklist.py` | Enforce the Billing Rollout Coordination Checklist output contract against the JSON Schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[project-manager]]
- [[change-request-pricing-rubric]]
- [[client-status-email-template-agency]]
- upstream playbook: `role-product-manager/Pricing experiment, hypothesis to result`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input completeness, owner named yes/no, decision materiality) to a concrete action, with each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about whether to run this methodology, route to a sibling methodology, or skip entirely.
