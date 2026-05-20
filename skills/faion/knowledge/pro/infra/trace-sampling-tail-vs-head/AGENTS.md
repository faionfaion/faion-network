---
slug: trace-sampling-tail-vs-head
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "12f9aa95cc852769"
summary: "Trace Sampling Tail Vs Head: produces a versioned, owner-signed artefact that closes the gap 'role-devops-engineer/Unified observability stack (logs + metrics + traces) in one weekend'."
tags: [trace-sampling-tail-vs-head, infra, pro]
---
# Trace Sampling Tail Vs Head

## Summary

**One-sentence:** Trace Sampling Tail Vs Head: produces a versioned, owner-signed artefact that closes the gap 'role-devops-engineer/Unified observability stack (logs + metrics + traces) in one weekend'.

**One-paragraph:** Addresses the gap surfaced by 'role-devops-engineer/Unified observability stack (logs + metrics + traces) in one weekend': Tail-based sampling via OTel Collector is the only thing that makes traces affordable at scale; no current methodology covers it. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a trace sampling tail vs head artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'role-devops-engineer/Unified observability stack (logs + metrics + traces) in one weekend' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working trace sampling tail vs head artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'role-devops-engineer/Unified observability stack (logs + metrics + traces) in one weekend' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/infra` | parent domain group — provides operating context for Trace Sampling Tail Vs Head |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules grounded in the cited gap | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/trace-sampling-tail-vs-head.json` | JSON schema for the Trace Sampling Tail Vs Head output contract |
| `templates/trace-sampling-tail-vs-head.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-trace-sampling-tail-vs-head.py` | Enforce Trace Sampling Tail Vs Head output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/infra/`
- upstream playbook: `role-devops-engineer/Unified observability stack (logs + metrics + traces) in one weekend`
- pro/infra/role-devops-engineer
