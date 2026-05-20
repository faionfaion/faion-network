---
slug: newsletter-issue-template-indie
tier: solo
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Newsletter Issue Template Indie: codified marketing practice that turns the recurring 'p2-indie-hacker/Weekly newsletter ideation + draft' decision into a repeatable, auditable artefact.
content_id: "498873df7ce01e4d"
tags: [newsletter-issue-template-indie, marketing, solo]
---
# Newsletter Issue Template Indie

## Summary

**One-sentence:** Newsletter Issue Template Indie: codified marketing practice that turns the recurring 'p2-indie-hacker/Weekly newsletter ideation + draft' decision into a repeatable, auditable artefact.

**One-paragraph:** Newsletter Issue Template Indie addresses the gap identified by the p2-indie-hacker/Weekly newsletter ideation + draft playbook: Existing newsletter-growth is strategic; no ready-to-fill weekly indie issue template (hook → story → lesson → CTA) sized ≤900 words. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of p2-indie-hacker/Weekly newsletter ideation + draft OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the p2-indie-hacker/Weekly newsletter ideation + draft task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/content-marketer` | parent role skill — provides the operating context for this methodology |

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
| `templates/newsletter-issue-template-indie.json` | JSON schema for the Newsletter Issue Template Indie output contract |
| `templates/newsletter-issue-template-indie.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-newsletter-issue-template-indie.py` | Enforce Newsletter Issue Template Indie output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/marketing/content-marketer/`
- upstream playbook: `p2-indie-hacker/Weekly newsletter ideation + draft`
