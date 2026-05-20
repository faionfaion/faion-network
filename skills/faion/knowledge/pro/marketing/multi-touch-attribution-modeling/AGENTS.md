---
slug: multi-touch-attribution-modeling
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Multi Touch Attribution Modeling: codified marketing practice that turns the recurring 'role-growth-marketing/Synthesis: Ship one piece of content into 10 channels with AI-assisted atomization' decision into a repeatable, auditable artefact.
content_id: "cb26c938ea7bbbac"
tags: [multi-touch-attribution-modeling, marketing, pro]
---
# Multi Touch Attribution Modeling

## Summary

**One-sentence:** Multi Touch Attribution Modeling: codified marketing practice that turns the recurring 'role-growth-marketing/Synthesis: Ship one piece of content into 10 channels with AI-assisted atomization' decision into a repeatable, auditable artefact.

**One-paragraph:** Multi Touch Attribution Modeling addresses the gap identified by the role-growth-marketing/Synthesis: Ship one piece of content into 10 channels with AI-assisted atomization playbook: `ads-attribution-models` exists but is paid-channel-only. Real growth marketers need a cross-channel multi-touch model (first-touch + linear + position-based + time-decay) that includes organic + email + community + dark-social. This is the single biggest pain mentioned in the brief ('attribution mess'). Without it, the entire growth-marketer sub-role can't prove what works. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-growth-marketing/Synthesis: Ship one piece of content into 10 channels with AI-assisted atomization OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-growth-marketing/Synthesis: Ship one piece of content into 10 channels with AI-assisted atomization task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer` | parent role skill — provides the operating context for this methodology |

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
| `templates/multi-touch-attribution-modeling.json` | JSON schema for the Multi Touch Attribution Modeling output contract |
| `templates/multi-touch-attribution-modeling.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-multi-touch-attribution-modeling.py` | Enforce Multi Touch Attribution Modeling output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/marketing/growth-marketer/`
- upstream playbook: `role-growth-marketing/Synthesis: Ship one piece of content into 10 channels with AI-assisted atomization`
