---
slug: vector-db-tuning-runbook
tier: geek
group: ai
domain: ai-core
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "6c599d599cd27835"
summary: "Vector Db Tuning Runbook: produces a versioned, owner-signed artefact that closes the gap 'role-ml-engineer/Vector DB query optimization pass'."
tags: [vector-db-tuning-runbook, ai, geek]
---
# Vector Db Tuning Runbook

## Summary

**One-sentence:** Vector Db Tuning Runbook: produces a versioned, owner-signed artefact that closes the gap 'role-ml-engineer/Vector DB query optimization pass'.

**One-paragraph:** Addresses the gap surfaced by 'role-ml-engineer/Vector DB query optimization pass': vector-db-* covers setup + monitoring; the recall/latency Pareto-walk loop is implicit. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a vector db tuning runbook artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'role-ml-engineer/Vector DB query optimization pass' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == geek or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working vector db tuning runbook artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'role-ml-engineer/Vector DB query optimization pass' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai` | parent domain group — provides operating context for Vector Db Tuning Runbook |

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
| `templates/vector-db-tuning-runbook.json` | JSON schema for the Vector Db Tuning Runbook output contract |
| `templates/vector-db-tuning-runbook.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vector-db-tuning-runbook.py` | Enforce Vector Db Tuning Runbook output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/ai/`
- upstream playbook: `role-ml-engineer/Vector DB query optimization pass`
- geek/ai/role-ml-engineer
