---
slug: capacity-bottleneck-checklist
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Capacity Bottleneck Checklist: codified engineering practice that turns the recurring 'role-software-architect/Capacity + cost-modelling exercise (pre-launch or scale-event)' decision into a repeatable, auditable artefact.
content_id: "712f4bcda3b2b6ff"
tags: [capacity-bottleneck-checklist, dev, pro]
---
# Capacity Bottleneck Checklist

## Summary

**One-sentence:** Capacity Bottleneck Checklist: codified engineering practice that turns the recurring 'role-software-architect/Capacity + cost-modelling exercise (pre-launch or scale-event)' decision into a repeatable, auditable artefact.

**One-paragraph:** Capacity Bottleneck Checklist addresses the gap identified by the role-software-architect/Capacity + cost-modelling exercise (pre-launch or scale-event) playbook: Capacity model lives or dies on whether you found the chokepoint (DB connections, queue throughput, gateway TLS, autoscale lag). A checklist is missing in the corpus. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-software-architect/Capacity + cost-modelling exercise (pre-launch or scale-event) OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-software-architect/Capacity + cost-modelling exercise (pre-launch or scale-event) task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/software-developer` | parent role skill — provides the operating context for this methodology |

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
| `templates/capacity-bottleneck-checklist.json` | JSON schema for the Capacity Bottleneck Checklist output contract |
| `templates/capacity-bottleneck-checklist.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-capacity-bottleneck-checklist.py` | Enforce Capacity Bottleneck Checklist output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/dev/`
- upstream playbook: `role-software-architect/Capacity + cost-modelling exercise (pre-launch or scale-event)`
