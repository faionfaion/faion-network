---
slug: lock-in-risk-scoring-rubric
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Lock In Risk Scoring Rubric: codified dev practice that turns the recurring 'role-software-architect/Technology evaluation + selection cycle' decision into a repeatable, auditable artefact.
content_id: "99d3bbc0bb0a06dc"
tags: [lock-in-risk-scoring-rubric, dev, pro]
---
# Lock In Risk Scoring Rubric

## Summary

**One-sentence:** Lock In Risk Scoring Rubric: codified dev practice that turns the recurring 'role-software-architect/Technology evaluation + selection cycle' decision into a repeatable, auditable artefact.

**One-paragraph:** Lock In Risk Scoring Rubric addresses the gap identified by the role-software-architect/Technology evaluation + selection cycle playbook: Vendor lock-in is rarely scored explicitly. A rubric (data portability, control-plane exit, hiring market, license) would harden evaluations. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-software-architect/Technology evaluation + selection cycle OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-software-architect/Technology evaluation + selection cycle task (last 30 days)
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
| `templates/lock-in-risk-scoring-rubric.json` | JSON schema for the Lock In Risk Scoring Rubric output contract |
| `templates/lock-in-risk-scoring-rubric.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-lock-in-risk-scoring-rubric.py` | Enforce Lock In Risk Scoring Rubric output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/dev/software-developer/`
- upstream playbook: `role-software-architect/Technology evaluation + selection cycle`
