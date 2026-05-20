---
slug: c4-drift-detection-from-iac
tier: geek
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: C4 Drift Detection From Iac: codified engineering practice that turns the recurring 'role-software-architect/Living architecture diagram refresh' decision into a repeatable, auditable artefact.
content_id: "d7f7dae8ee37c4b5"
tags: [c4-drift-detection-from-iac, dev, geek]
---
# C4 Drift Detection From Iac

## Summary

**One-sentence:** C4 Drift Detection From Iac: codified engineering practice that turns the recurring 'role-software-architect/Living architecture diagram refresh' decision into a repeatable, auditable artefact.

**One-paragraph:** C4 Drift Detection From Iac addresses the gap identified by the role-software-architect/Living architecture diagram refresh playbook: C4 model methodology exists at solo tier but doesn't address how to diff diagram against IaC + service registry — the core problem of 'diagram lies'. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-software-architect/Living architecture diagram refresh OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == geek or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-software-architect/Living architecture diagram refresh task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/dev/software-developer` | parent role skill — provides the operating context for this methodology |

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
| `templates/c4-drift-detection-from-iac.json` | JSON schema for the C4 Drift Detection From Iac output contract |
| `templates/c4-drift-detection-from-iac.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-c4-drift-detection-from-iac.py` | Enforce C4 Drift Detection From Iac output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/dev/`
- upstream playbook: `role-software-architect/Living architecture diagram refresh`
