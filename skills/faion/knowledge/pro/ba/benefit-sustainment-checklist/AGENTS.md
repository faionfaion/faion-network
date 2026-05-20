---
slug: benefit-sustainment-checklist
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Benefit Sustainment Checklist: codified business-analysis practice that turns the recurring 'role-business-analyst/Process improvement initiative (8 weeks)' decision into a repeatable, auditable artefact.
content_id: "e98561cc87e53ce6"
tags: [benefit-sustainment-checklist, ba, pro]
---
# Benefit Sustainment Checklist

## Summary

**One-sentence:** Benefit Sustainment Checklist: codified business-analysis practice that turns the recurring 'role-business-analyst/Process improvement initiative (8 weeks)' decision into a repeatable, auditable artefact.

**One-paragraph:** Benefit Sustainment Checklist addresses the gap identified by the role-business-analyst/Process improvement initiative (8 weeks) playbook: 'benefits-realization' covers measurement but not sustainment. Need a checklist for embedding gains: governance owner, review cadence, retraining triggers, regression test cases, contractual SLA links. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-business-analyst/Process improvement initiative (8 weeks) OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-business-analyst/Process improvement initiative (8 weeks) task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/business-analyst` | parent role skill — provides the operating context for this methodology |

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
| `templates/benefit-sustainment-checklist.json` | JSON schema for the Benefit Sustainment Checklist output contract |
| `templates/benefit-sustainment-checklist.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-benefit-sustainment-checklist.py` | Enforce Benefit Sustainment Checklist output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/ba/`
- upstream playbook: `role-business-analyst/Process improvement initiative (8 weeks)`
