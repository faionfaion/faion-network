---
slug: capacity-vs-ask-balancer
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Capacity vs Ask Balancer: codified delivery-management practice that turns the recurring 'role-product-manager/Quarter planning + OKR cascade' decision into a repeatable, auditable artefact.
content_id: "53fc835c5f7eb836"
tags: [capacity-vs-ask-balancer, pm, pro]
---
# Capacity vs Ask Balancer

## Summary

**One-sentence:** Capacity vs Ask Balancer: codified delivery-management practice that turns the recurring 'role-product-manager/Quarter planning + OKR cascade' decision into a repeatable, auditable artefact.

**One-paragraph:** Capacity vs Ask Balancer addresses the gap identified by the role-product-manager/Quarter planning + OKR cascade playbook: RICE / MoSCoW prioritise items but do not reconcile total ask against eng + design capacity. PM-level reality check absent from corpus. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-product-manager/Quarter planning + OKR cascade OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-product-manager/Quarter planning + OKR cascade task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/project-manager` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-headroom-floor | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Template fill, bounded transformation |
| `synthesize_decision` | sonnet | Per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/capacity-vs-ask-balancer.json` | JSON schema for the Capacity vs Ask Balancer output contract |
| `templates/capacity-vs-ask-balancer.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-capacity-vs-ask-balancer.py` | Enforce Capacity vs Ask Balancer output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/pm/`
- upstream playbook: `role-product-manager/Quarter planning + OKR cascade`
