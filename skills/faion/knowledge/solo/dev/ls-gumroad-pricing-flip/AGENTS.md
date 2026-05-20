---
slug: ls-gumroad-pricing-flip
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Ls Gumroad Pricing Flip: codified dev practice that turns the recurring 'p2-indie-hacker/Pricing experiment toggle' decision into a repeatable, auditable artefact.
content_id: "0edfaaa01e8f6d43"
tags: [ls-gumroad-pricing-flip, dev, solo]
---
# Ls Gumroad Pricing Flip

## Summary

**One-sentence:** Ls Gumroad Pricing Flip: codified dev practice that turns the recurring 'p2-indie-hacker/Pricing experiment toggle' decision into a repeatable, auditable artefact.

**One-paragraph:** Ls Gumroad Pricing Flip addresses the gap identified by the p2-indie-hacker/Pricing experiment toggle playbook: Stripe-integration-basics exists but indie tools-of-choice Lemon Squeezy / Gumroad have their own pricing-update mechanics not covered. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of p2-indie-hacker/Pricing experiment toggle OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the p2-indie-hacker/Pricing experiment toggle task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-developer` | parent role skill — provides the operating context for this methodology |

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
| `templates/ls-gumroad-pricing-flip.json` | JSON schema for the Ls Gumroad Pricing Flip output contract |
| `templates/ls-gumroad-pricing-flip.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ls-gumroad-pricing-flip.py` | Enforce Ls Gumroad Pricing Flip output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/dev/software-developer/`
- upstream playbook: `p2-indie-hacker/Pricing experiment toggle`
