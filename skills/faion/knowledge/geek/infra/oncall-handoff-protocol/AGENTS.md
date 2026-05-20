---
slug: oncall-handoff-protocol
tier: geek
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Oncall Handoff Protocol: codified infra practice that turns the recurring 'p6-product-dev-team/Cross-role handoff: PM -> Architect -> Dev -> QA -> DevOps in one loop' decision into a repeatable, auditable artefact.
content_id: "8ff841aabf1d8aa2"
tags: [oncall-handoff-protocol, infra, geek]
---
# Oncall Handoff Protocol

## Summary

**One-sentence:** Oncall Handoff Protocol: codified infra practice that turns the recurring 'p6-product-dev-team/Cross-role handoff: PM -> Architect -> Dev -> QA -> DevOps in one loop' decision into a repeatable, auditable artefact.

**One-paragraph:** Oncall Handoff Protocol addresses the gap identified by the p6-product-dev-team/Cross-role handoff: PM -> Architect -> Dev -> QA -> DevOps in one loop playbook: Cross-cutting atomic task we surfaced in the angle prompt but couldn't fit into a playbook above without redundancy. P6 teams need a concrete handoff format (open incidents, suppressed alerts, scheduled work, known-fragile services). Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

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
| `templates/oncall-handoff-protocol.json` | JSON schema for the Oncall Handoff Protocol output contract |
| `templates/oncall-handoff-protocol.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-oncall-handoff-protocol.py` | Enforce Oncall Handoff Protocol output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/infra/devops-engineer/`
- upstream playbook: `p6-product-dev-team/Cross-role handoff: PM -> Architect -> Dev -> QA -> DevOps in one loop`
