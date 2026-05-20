---
slug: niche-scorecard
tier: pro
group: research
domain: research
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Niche Scorecard: codified research practice that turns the recurring 'p3-technical-freelancer/Specialty niche pivot (8-12 weeks generalist to specialist)' decision into a repeatable, auditable artefact.
content_id: "bb0f7d8d789a2e64"
tags: [niche-scorecard, research, pro]
---
# Niche Scorecard

## Summary

**One-sentence:** Niche Scorecard: codified research practice that turns the recurring 'p3-technical-freelancer/Specialty niche pivot (8-12 weeks generalist to specialist)' decision into a repeatable, auditable artefact.

**One-paragraph:** Niche Scorecard addresses the gap identified by the p3-technical-freelancer/Specialty niche pivot (8-12 weeks generalist to specialist) playbook: market-researcher exists but a freelancer needs a tighter 5-dimension scorecard (demand, fit, ceiling, defensibility, distribution) sized for a weekend, not a research sprint. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of p3-technical-freelancer/Specialty niche pivot (8-12 weeks generalist to specialist) OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the p3-technical-freelancer/Specialty niche pivot (8-12 weeks generalist to specialist) task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/research/researcher` | parent role skill — provides the operating context for this methodology |

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
| `templates/niche-scorecard.json` | JSON schema for the Niche Scorecard output contract |
| `templates/niche-scorecard.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-niche-scorecard.py` | Enforce Niche Scorecard output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/research/researcher/`
- upstream playbook: `p3-technical-freelancer/Specialty niche pivot (8-12 weeks generalist to specialist)`
