---
slug: anti-slop-rubric
tier: geek
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Anti Slop Rubric: codified growth-marketing practice that turns the recurring 'role-growth-marketing/Content Engine Build from Zero (12 weeks)' decision into a repeatable, auditable artefact.
content_id: "96087030558f7f7b"
tags: [anti-slop-rubric, marketing, geek]
---
# Anti Slop Rubric

## Summary

**One-sentence:** Anti Slop Rubric: codified growth-marketing practice that turns the recurring 'role-growth-marketing/Content Engine Build from Zero (12 weeks)' decision into a repeatable, auditable artefact.

**One-paragraph:** Anti Slop Rubric addresses the gap identified by the role-growth-marketing/Content Engine Build from Zero (12 weeks) playbook: AI-assisted content pipelines without explicit anti-slop guardrails produce plausible-but-unrankable posts. Need a concrete rubric and review SOP — this is the user's stated #1 pain point. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-growth-marketing/Content Engine Build from Zero (12 weeks) OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == geek or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-growth-marketing/Content Engine Build from Zero (12 weeks) task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/marketing/marketing-manager` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-detector-first, r5-conversion-window | ~900 |
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
| `templates/anti-slop-rubric.json` | JSON schema for the Anti Slop Rubric output contract |
| `templates/anti-slop-rubric.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-anti-slop-rubric.py` | Enforce Anti Slop Rubric output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/marketing/`
- upstream playbook: `role-growth-marketing/Content Engine Build from Zero (12 weeks)`
