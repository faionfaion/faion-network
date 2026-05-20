---
slug: new-dependency-risk-checklist
tier: geek
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: New Dependency Risk Checklist: codified dev practice that turns the recurring 'p6-product-dev-team/Security review for new dependency' decision into a repeatable, auditable artefact.
content_id: "836ec61c48d0a42e"
tags: [new-dependency-risk-checklist, dev, geek]
---
# New Dependency Risk Checklist

## Summary

**One-sentence:** New Dependency Risk Checklist: codified dev practice that turns the recurring 'p6-product-dev-team/Security review for new dependency' decision into a repeatable, auditable artefact.

**One-paragraph:** New Dependency Risk Checklist addresses the gap identified by the p6-product-dev-team/Security review for new dependency playbook: Supply-chain scan exists; the operational human-side checklist (alts considered, ADR threshold, ownership) is missing. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of p6-product-dev-team/Security review for new dependency OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == geek or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the p6-product-dev-team/Security review for new dependency task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/dev/software-developer` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-traceable-decision | ~900 |
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
| `templates/new-dependency-risk-checklist.json` | JSON schema for the New Dependency Risk Checklist output contract |
| `templates/new-dependency-risk-checklist.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-new-dependency-risk-checklist.py` | Enforce New Dependency Risk Checklist output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/dev/software-developer/`
- upstream playbook: `p6-product-dev-team/Security review for new dependency`
