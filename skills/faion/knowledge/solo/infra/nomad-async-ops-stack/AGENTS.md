---
slug: nomad-async-ops-stack
tier: solo
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Nomad Async Ops Stack: codified infra practice that turns the recurring 'p2-indie-hacker/Multi-product portfolio rotation: ship N small bets per year' decision into a repeatable, auditable artefact.
content_id: "e2359b3ca2b092f0"
tags: [nomad-async-ops-stack, infra, solo]
---
# Nomad Async Ops Stack

## Summary

**One-sentence:** Nomad Async Ops Stack: codified infra practice that turns the recurring 'p2-indie-hacker/Multi-product portfolio rotation: ship N small bets per year' decision into a repeatable, auditable artefact.

**One-paragraph:** Nomad Async Ops Stack addresses the gap identified by the p2-indie-hacker/Multi-product portfolio rotation: ship N small bets per year playbook: Maya is a digital nomad on flaky Bali/Mexico City wifi. faion has no methodology for running solo ops fully async + offline-tolerant: editor stack, payment ops timezone strategy, customer-support SLA across 12h delta. Distinctly indie-flavored ops skill. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of p2-indie-hacker/Multi-product portfolio rotation: ship N small bets per year OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the p2-indie-hacker/Multi-product portfolio rotation: ship N small bets per year task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/infra/server-craft` | parent role skill — provides the operating context for this methodology |

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
| `templates/nomad-async-ops-stack.json` | JSON schema for the Nomad Async Ops Stack output contract |
| `templates/nomad-async-ops-stack.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-nomad-async-ops-stack.py` | Enforce Nomad Async Ops Stack output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/infra/server-craft/`
- upstream playbook: `p2-indie-hacker/Multi-product portfolio rotation: ship N small bets per year`
