---
slug: validation-paralysis-breaker
tier: solo
group: research
domain: research
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "1d2d2bb9b1ae0ded"
summary: "Validation Paralysis Breaker: produces a versioned, owner-signed artefact that closes the gap 'p2-indie-hacker/Tweet-to-launch sprint: idea to paying user in 3 weeks'."
tags: [validation-paralysis-breaker, research, solo]
---
# Validation Paralysis Breaker

## Summary

**One-sentence:** Validation Paralysis Breaker: produces a versioned, owner-signed artefact that closes the gap 'p2-indie-hacker/Tweet-to-launch sprint: idea to paying user in 3 weeks'.

**One-paragraph:** Addresses the gap surfaced by 'p2-indie-hacker/Tweet-to-launch sprint: idea to paying user in 3 weeks': The persona's #1 cognitive failure mode is validation paralysis. faion has problem-validation-2026 but nothing that names the anti-pattern and gives a forced-decision protocol (e.g., '72h validation budget then ship anyway'). Worth one opinionated methodology. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a validation paralysis breaker artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'p2-indie-hacker/Tweet-to-launch sprint: idea to paying user in 3 weeks' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working validation paralysis breaker artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'p2-indie-hacker/Tweet-to-launch sprint: idea to paying user in 3 weeks' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/research/research` | parent domain group — provides operating context for Validation Paralysis Breaker |

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
| `templates/validation-paralysis-breaker.json` | JSON schema for the Validation Paralysis Breaker output contract |
| `templates/validation-paralysis-breaker.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-validation-paralysis-breaker.py` | Enforce Validation Paralysis Breaker output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/research/`
- upstream playbook: `p2-indie-hacker/Tweet-to-launch sprint: idea to paying user in 3 weeks`
- solo/research/p2-indie-hacker
