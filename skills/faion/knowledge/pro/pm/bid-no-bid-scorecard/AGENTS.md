---
slug: bid-no-bid-scorecard
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Bid No Bid Scorecard: codified delivery-management practice that turns the recurring 'p4-outsource-specialist/Fixed-price bid discovery + estimation (1 week)' decision into a repeatable, auditable artefact.
content_id: "2a0bffe8581563a6"
tags: [bid-no-bid-scorecard, pm, pro]
---
# Bid No Bid Scorecard

## Summary

**One-sentence:** Bid No Bid Scorecard: codified delivery-management practice that turns the recurring 'p4-outsource-specialist/Fixed-price bid discovery + estimation (1 week)' decision into a repeatable, auditable artefact.

**One-paragraph:** Bid No Bid Scorecard addresses the gap identified by the p4-outsource-specialist/Fixed-price bid discovery + estimation (1 week) playbook: There is no scoring framework for whether to bid at all — margin, fit, compliance burden, AI-leverage potential. Outsource specialists carry this in their head; it should be a methodology. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of p4-outsource-specialist/Fixed-price bid discovery + estimation (1 week) OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the p4-outsource-specialist/Fixed-price bid discovery + estimation (1 week) task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/project-manager` | parent role skill — provides the operating context for this methodology |

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
| `templates/bid-no-bid-scorecard.json` | JSON schema for the Bid No Bid Scorecard output contract |
| `templates/bid-no-bid-scorecard.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-bid-no-bid-scorecard.py` | Enforce Bid No Bid Scorecard output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/pm/`
- upstream playbook: `p4-outsource-specialist/Fixed-price bid discovery + estimation (1 week)`
