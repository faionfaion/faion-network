---
slug: on-call-shift-retro-cadence
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: On Call Shift Retro Cadence: codified infra practice that turns the recurring 'role-devops-engineer/On-call handoff' decision into a repeatable, auditable artefact.
content_id: "b9406c8094739cb8"
tags: [on-call-shift-retro-cadence, infra, pro]
---
# On Call Shift Retro Cadence

## Summary

**One-sentence:** On Call Shift Retro Cadence: codified infra practice that turns the recurring 'role-devops-engineer/On-call handoff' decision into a repeatable, auditable artefact.

**One-paragraph:** On Call Shift Retro Cadence addresses the gap identified by the role-devops-engineer/On-call handoff playbook: inc-postmortem covers incidents; no methodology for the lighter-weight per-shift retro on noise + toil patterns. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-devops-engineer/On-call handoff OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-devops-engineer/On-call handoff task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer` | parent role skill — provides the operating context for this methodology |

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
| `templates/on-call-shift-retro-cadence.json` | JSON schema for the On Call Shift Retro Cadence output contract |
| `templates/on-call-shift-retro-cadence.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-on-call-shift-retro-cadence.py` | Enforce On Call Shift Retro Cadence output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/infra/devops-engineer/`
- upstream playbook: `role-devops-engineer/On-call handoff`
