---
slug: auto-rollback-policy-design
tier: geek
group: ai
domain: ai-core
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Auto Rollback Policy Design: codified AI-system reliability practice that turns the recurring 'role-ml-engineer/Migrate LLM provider / model generation' decision into a repeatable, auditable artefact.
content_id: "06d46b3e355384b7"
tags: [auto-rollback-policy-design, ai, geek]
---
# Auto Rollback Policy Design

## Summary

**One-sentence:** Auto Rollback Policy Design: codified AI-system reliability practice that turns the recurring 'role-ml-engineer/Migrate LLM provider / model generation' decision into a repeatable, auditable artefact.

**One-paragraph:** Auto Rollback Policy Design addresses the gap identified by the role-ml-engineer/Migrate LLM provider / model generation playbook: How to define and implement quality-score-based auto-rollback for AI features. Today this falls to ad-hoc on-call decisions. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-ml-engineer/Migrate LLM provider / model generation OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == geek or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-ml-engineer/Migrate LLM provider / model generation task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer` | parent role skill — provides the operating context for this methodology |

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
| `templates/auto-rollback-policy-design.json` | JSON schema for the Auto Rollback Policy Design output contract |
| `templates/auto-rollback-policy-design.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-auto-rollback-policy-design.py` | Enforce Auto Rollback Policy Design output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/ai/`
- upstream playbook: `role-ml-engineer/Migrate LLM provider / model generation`
