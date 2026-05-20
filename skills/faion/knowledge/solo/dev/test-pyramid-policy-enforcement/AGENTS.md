---
slug: test-pyramid-policy-enforcement
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "cee4b13ddebf77ea"
summary: "Test Pyramid Policy Enforcement: produces a versioned, owner-signed artefact that closes the gap 'role-qa-engineer/Test pyramid rebalance: too-many-e2e to contract + unit'."
tags: [test-pyramid-policy-enforcement, dev, solo]
---
# Test Pyramid Policy Enforcement

## Summary

**One-sentence:** Test Pyramid Policy Enforcement: produces a versioned, owner-signed artefact that closes the gap 'role-qa-engineer/Test pyramid rebalance: too-many-e2e to contract + unit'.

**One-paragraph:** Addresses the gap surfaced by 'role-qa-engineer/Test pyramid rebalance: too-many-e2e to contract + unit': After a pyramid rebalance, teams need a 'no new e2e without justification' enforcement rule + PR template — currently missing. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a test pyramid policy enforcement artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'role-qa-engineer/Test pyramid rebalance: too-many-e2e to contract + unit' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working test pyramid policy enforcement artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'role-qa-engineer/Test pyramid rebalance: too-many-e2e to contract + unit' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/dev` | parent domain group — provides operating context for Test Pyramid Policy Enforcement |

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
| `templates/test-pyramid-policy-enforcement.json` | JSON schema for the Test Pyramid Policy Enforcement output contract |
| `templates/test-pyramid-policy-enforcement.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-test-pyramid-policy-enforcement.py` | Enforce Test Pyramid Policy Enforcement output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/dev/`
- upstream playbook: `role-qa-engineer/Test pyramid rebalance: too-many-e2e to contract + unit`
- solo/dev/role-qa-engineer
