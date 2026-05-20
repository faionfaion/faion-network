---
slug: on-call-rotation-setup
tier: geek
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: On Call Rotation Setup: codified infra practice that turns the recurring 'p6-product-dev-team/Cross-role handoff: PM -> Architect -> Dev -> QA -> DevOps in one loop' decision into a repeatable, auditable artefact.
content_id: "8abb8aaa81ab1144"
tags: [on-call-rotation-setup, infra, geek]
---
# On Call Rotation Setup

## Summary

**One-sentence:** On Call Rotation Setup: codified infra practice that turns the recurring 'p6-product-dev-team/Cross-role handoff: PM -> Architect -> Dev -> QA -> DevOps in one loop' decision into a repeatable, auditable artefact.

**One-paragraph:** On Call Rotation Setup addresses the gap identified by the p6-product-dev-team/Cross-role handoff: PM -> Architect -> Dev -> QA -> DevOps in one loop playbook: DORA-metrics and runbooks exist. Nothing on setting up the rotation itself: pager schedule, comp policy (pay or comp time), follow-the-sun if EU+US, hand-off ritual, escalation policy. Critical for 2-10 person teams as soon as one customer pays for uptime Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of p6-product-dev-team/Cross-role handoff: PM -> Architect -> Dev -> QA -> DevOps in one loop OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == geek or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the p6-product-dev-team/Cross-role handoff: PM -> Architect -> Dev -> QA -> DevOps in one loop task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/infra/devops-engineer` | parent role skill — provides the operating context for this methodology |

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
| `templates/on-call-rotation-setup.json` | JSON schema for the On Call Rotation Setup output contract |
| `templates/on-call-rotation-setup.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-on-call-rotation-setup.py` | Enforce On Call Rotation Setup output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/infra/devops-engineer/`
- upstream playbook: `p6-product-dev-team/Cross-role handoff: PM -> Architect -> Dev -> QA -> DevOps in one loop`
