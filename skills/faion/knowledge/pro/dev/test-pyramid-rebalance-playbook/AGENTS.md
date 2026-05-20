---
slug: test-pyramid-rebalance-playbook
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "2dbba572cb04e2ca"
summary: "Test Pyramid Rebalance Playbook: produces a versioned, owner-signed artefact that closes the gap 'role-qa-engineer/Modernize a 2018-era QA suite into AI-augmented test ops'."
tags: [test-pyramid-rebalance-playbook, dev, pro]
---
# Test Pyramid Rebalance Playbook

## Summary

**One-sentence:** Test Pyramid Rebalance Playbook: produces a versioned, owner-signed artefact that closes the gap 'role-qa-engineer/Modernize a 2018-era QA suite into AI-augmented test ops'.

**One-paragraph:** Addresses the gap surfaced by 'role-qa-engineer/Modernize a 2018-era QA suite into AI-augmented test ops': Faion's testing-patterns mentions Test Pyramid as a pattern but never as a system to manage. Real teams arrive ice-cream-cone-shaped (heavy E2E, anaemic unit/integration). A QA engineer needs a rebalance methodology: how to measure shape, what target shape fits which architecture (monolith vs micro vs LLM-augmented), what to delete, what to push down. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a test pyramid rebalance playbook artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'role-qa-engineer/Modernize a 2018-era QA suite into AI-augmented test ops' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working test pyramid rebalance playbook artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'role-qa-engineer/Modernize a 2018-era QA suite into AI-augmented test ops' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/dev` | parent domain group — provides operating context for Test Pyramid Rebalance Playbook |

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
| `templates/test-pyramid-rebalance-playbook.json` | JSON schema for the Test Pyramid Rebalance Playbook output contract |
| `templates/test-pyramid-rebalance-playbook.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-test-pyramid-rebalance-playbook.py` | Enforce Test Pyramid Rebalance Playbook output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/dev/`
- upstream playbook: `role-qa-engineer/Modernize a 2018-era QA suite into AI-augmented test ops`
- pro/dev/role-qa-engineer
