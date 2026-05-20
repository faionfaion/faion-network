---
slug: ai-post-mortem-template
tier: pro
group: ai
domain: ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Ai Post Mortem Template: codified AI-system reliability practice that turns the recurring 'role-ml-engineer/Run an AI-feature incident from page to post-mortem' decision into a repeatable, auditable artefact.
content_id: "44cb71792f6b6bdc"
tags: [ai-post-mortem-template, ai, pro]
---
# Ai Post Mortem Template

## Summary

**One-sentence:** Ai Post Mortem Template: codified AI-system reliability practice that turns the recurring 'role-ml-engineer/Run an AI-feature incident from page to post-mortem' decision into a repeatable, auditable artefact.

**One-paragraph:** Ai Post Mortem Template addresses the gap identified by the role-ml-engineer/Run an AI-feature incident from page to post-mortem playbook: Generic post-mortems don't ask the right questions for AI incidents (was it deterministic, can we reproduce on golden set, what regression test closes the loop, did we add a new golden sample). Need an AI-specific template. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-ml-engineer/Run an AI-feature incident from page to post-mortem OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-ml-engineer/Run an AI-feature incident from page to post-mortem task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ai/ml-engineer` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-llm-grounding, r5-blameless | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 7 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Template fill, bounded transformation |
| `synthesize_decision` | sonnet | Per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/ai-post-mortem-template.json` | JSON schema for the Ai Post Mortem Template output contract |
| `templates/ai-post-mortem-template.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-post-mortem-template.py` | Enforce Ai Post Mortem Template output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/ai/`
- upstream playbook: `role-ml-engineer/Run an AI-feature incident from page to post-mortem`
- external: [Allspaw 2012](https://www.kitchensoap.com/2012/10/25/on-being-a-senior-engineer/) · [Google SRE Postmortem chapter](https://sre.google/sre-book/postmortem-culture/)
