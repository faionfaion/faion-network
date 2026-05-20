---
slug: bid-no-bid-scoring-rubric
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Bid No Bid Scoring Rubric: codified business-analysis practice that turns the recurring 'role-business-analyst/Pre-bid discovery for a fixed-price engagement (P4)' decision into a repeatable, auditable artefact.
content_id: "8571d0fb7a3c09ec"
tags: [bid-no-bid-scoring-rubric, ba, pro]
---
# Bid No Bid Scoring Rubric

## Summary

**One-sentence:** Bid No Bid Scoring Rubric: codified business-analysis practice that turns the recurring 'role-business-analyst/Pre-bid discovery for a fixed-price engagement (P4)' decision into a repeatable, auditable artefact.

**One-paragraph:** Bid No Bid Scoring Rubric addresses the gap identified by the role-business-analyst/Pre-bid discovery for a fixed-price engagement (P4) playbook: Pre-sales BAs need a structured rubric for bid/no-bid decisions. Currently judgement-only. Standardised scoring reduces bad-fit clients which drives project-margin failures. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-business-analyst/Pre-bid discovery for a fixed-price engagement (P4) OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-business-analyst/Pre-bid discovery for a fixed-price engagement (P4) task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/business-analyst` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-detector-first | ~900 |
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
| `templates/bid-no-bid-scoring-rubric.json` | JSON schema for the Bid No Bid Scoring Rubric output contract |
| `templates/bid-no-bid-scoring-rubric.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-bid-no-bid-scoring-rubric.py` | Enforce Bid No Bid Scoring Rubric output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/ba/`
- upstream playbook: `role-business-analyst/Pre-bid discovery for a fixed-price engagement (P4)`
