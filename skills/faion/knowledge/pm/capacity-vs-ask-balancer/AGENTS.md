# Capacity vs Ask Balancer

## Summary

**One-sentence:** Generates a quarter-level decision record that reconciles requested scope against realistic capacity — accepted, deferred, dropped lines with rationale.

**One-paragraph:** Capacity vs Ask Balancer addresses the gap identified by the `role-product-manager/Quarter planning + OKR cascade` playbook: OKR cascades collect more asks than capacity allows. Without an explicit balancer, low-leverage asks crowd out the high-leverage ones by default. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned `decision-record` artefact carrying a named accountable owner, input citations, and a review date — downstream agents and human reviewers consume it without re-deriving the rationale.

**Ефективно для:**

- Decision record з options, рішенням, rationale і default-if-silent.
- Іменований власник — жодного 'team' / 'we' як вирішувача.
- Зв'язана з input-артефактами по path/URL, без вільної прози без цитувань.
- Версіонована; bumping required при матеріальній зміні рішення.

## Applies If (ALL must hold)

- Task is an instance of `role-product-manager/Quarter planning + OKR cascade` OR a closely-adjacent variant in the same engagement shape.
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
| Recent context for the `role-product-manager/Quarter planning + OKR cascade` task (last 30 days) | Markdown / chat log | engagement notes |
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
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for `decision-record` shape + valid/invalid/forbidden examples | 800 |
| `content/03-failure-modes.xml` | essential | 3+ antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate per step | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping observable signals to a rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Template-fill of inputs from named sources; bounded transformation. |
| `synthesize-decision-record` | sonnet | Per-instance judgment over bounded inputs to fill the `decision-record` shape. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high (regulatory / large €). |

## Templates

| File | Purpose |
|------|---------|
| `templates/capacity-vs-ask-balancer.json` | JSON Schema (draft-07) for the Capacity vs Ask Balancer output contract |
| `templates/capacity-vs-ask-balancer.md` | Markdown skeleton with the required fields for the Capacity vs Ask Balancer artefact |
| `templates/capacity-vs-ask-balancer.example.json` | Worked filled-in example of a valid Capacity vs Ask Balancer artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-capacity-vs-ask-balancer.py` | Enforce the Capacity vs Ask Balancer output contract against the JSON Schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[project-manager]]
- [[change-request-pricing-rubric]]
- [[client-status-email-template-agency]]
- upstream playbook: `role-product-manager/Quarter planning + OKR cascade`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input completeness, owner named yes/no, decision materiality) to a concrete action, with each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about whether to run this methodology, route to a sibling methodology, or skip entirely.
