---
slug: anti-theater-retro-guardrails
tier: geek
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Anti Theater Retro Guardrails: codified delivery-management practice that turns the recurring 'p6-product-dev-team/Bi-weekly retro with mistake-memory feedback' decision into a repeatable, auditable artefact.
content_id: "869e2fa735b29d50"
tags: [anti-theater-retro-guardrails, pm, geek]
---
# Anti Theater Retro Guardrails

## Summary

**One-sentence:** Anti Theater Retro Guardrails: codified delivery-management practice that turns the recurring 'p6-product-dev-team/Bi-weekly retro with mistake-memory feedback' decision into a repeatable, auditable artefact.

**One-paragraph:** Anti Theater Retro Guardrails addresses the gap identified by the p6-product-dev-team/Bi-weekly retro with mistake-memory feedback playbook: Scrum-ceremonies covers happy path; the failure mode (status theater retros) has no opinionated guardrail page. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of p6-product-dev-team/Bi-weekly retro with mistake-memory feedback OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == geek or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the p6-product-dev-team/Bi-weekly retro with mistake-memory feedback task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/pm/project-manager` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned | ~900 |
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
| `templates/anti-theater-retro-guardrails.json` | JSON schema for the Anti Theater Retro Guardrails output contract |
| `templates/anti-theater-retro-guardrails.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-anti-theater-retro-guardrails.py` | Enforce Anti Theater Retro Guardrails output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/pm/`
- upstream playbook: `p6-product-dev-team/Bi-weekly retro with mistake-memory feedback`
