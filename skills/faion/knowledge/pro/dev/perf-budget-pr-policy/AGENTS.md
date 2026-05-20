---
slug: perf-budget-pr-policy
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Perf Budget Pr Policy: codified dev practice that turns the recurring 'role-qa-engineer/Performance + load test program rollout' decision into a repeatable, auditable artefact.
content_id: "23ca34f968ce6ef7"
tags: [perf-budget-pr-policy, dev, pro]
---
# Perf Budget Pr Policy

## Summary

**One-sentence:** Perf Budget Pr Policy: codified dev practice that turns the recurring 'role-qa-engineer/Performance + load test program rollout' decision into a repeatable, auditable artefact.

**One-paragraph:** Perf Budget Pr Policy addresses the gap identified by the role-qa-engineer/Performance + load test program rollout playbook: Perf-test methodologies cover how to run; the PR-budget governance layer (block/warn/waive thresholds) is missing. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-qa-engineer/Performance + load test program rollout OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-qa-engineer/Performance + load test program rollout task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/software-developer` | parent role skill — provides the operating context for this methodology |

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
| `templates/perf-budget-pr-policy.json` | JSON schema for the Perf Budget Pr Policy output contract |
| `templates/perf-budget-pr-policy.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-perf-budget-pr-policy.py` | Enforce Perf Budget Pr Policy output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/dev/software-developer/`
- upstream playbook: `role-qa-engineer/Performance + load test program rollout`
