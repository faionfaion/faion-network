---
slug: technology-evaluation-rubric
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "6a02008d6fe9c4fb"
summary: "Technology Evaluation Rubric: produces a versioned, owner-signed artefact that closes the gap 'role-software-architect/Cost + latency budget BEFORE design freeze'."
tags: [technology-evaluation-rubric, dev, pro]
---
# Technology Evaluation Rubric

## Summary

**One-sentence:** Technology Evaluation Rubric: produces a versioned, owner-signed artefact that closes the gap 'role-software-architect/Cost + latency budget BEFORE design freeze'.

**One-paragraph:** Addresses the gap surfaced by 'role-software-architect/Cost + latency budget BEFORE design freeze': decision-tree-tech-stack covers stack picking; trade-off-build-vs-buy covers build/buy. A scored rubric (maturity, license, ecosystem, hire-ability, exit cost, AI-friendliness) for evaluating individual tools (vector DB, queue, observability vendor) is missing. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a technology evaluation rubric artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'role-software-architect/Cost + latency budget BEFORE design freeze' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working technology evaluation rubric artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'role-software-architect/Cost + latency budget BEFORE design freeze' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/dev` | parent domain group — provides operating context for Technology Evaluation Rubric |

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
| `templates/technology-evaluation-rubric.json` | JSON schema for the Technology Evaluation Rubric output contract |
| `templates/technology-evaluation-rubric.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-technology-evaluation-rubric.py` | Enforce Technology Evaluation Rubric output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/dev/`
- upstream playbook: `role-software-architect/Cost + latency budget BEFORE design freeze`
- pro/dev/role-software-architect
