---
slug: paid-test-task-scoring-rubric
tier: pro
group: comms
domain: comms
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Paid Test Task Scoring Rubric: codified comms practice that turns the recurring 'p5-micro-agency-founder/Hire and onboard a new contractor (3–5 weeks)' decision into a repeatable, auditable artefact.
content_id: "5b945bd316b29424"
tags: [paid-test-task-scoring-rubric, comms, pro]
---
# Paid Test Task Scoring Rubric

## Summary

**One-sentence:** Paid Test Task Scoring Rubric: codified comms practice that turns the recurring 'p5-micro-agency-founder/Hire and onboard a new contractor (3–5 weeks)' decision into a repeatable, auditable artefact.

**One-paragraph:** Paid Test Task Scoring Rubric addresses the gap identified by the p5-micro-agency-founder/Hire and onboard a new contractor (3–5 weeks) playbook: Interview methodology exists but the paid-test-task pattern (real-shaped paid screen, ~$100–$300) is missing and is the highest-signal screen for contractors. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of p5-micro-agency-founder/Hire and onboard a new contractor (3–5 weeks) OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the p5-micro-agency-founder/Hire and onboard a new contractor (3–5 weeks) task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/comms/hr-recruiter` | parent role skill — provides the operating context for this methodology |

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
| `templates/paid-test-task-scoring-rubric.json` | JSON schema for the Paid Test Task Scoring Rubric output contract |
| `templates/paid-test-task-scoring-rubric.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-paid-test-task-scoring-rubric.py` | Enforce Paid Test Task Scoring Rubric output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/comms/hr-recruiter/`
- upstream playbook: `p5-micro-agency-founder/Hire and onboard a new contractor (3–5 weeks)`
