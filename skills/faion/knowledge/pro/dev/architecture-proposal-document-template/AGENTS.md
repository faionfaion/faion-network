---
slug: architecture-proposal-document-template
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Architecture Proposal Document Template: codified engineering practice that turns the recurring 'role-software-architect/Greenfield architecture proposal — concept to signed-off design pack' decision into a repeatable, auditable artefact.
content_id: "e6537ccf5e2523f9"
tags: [architecture-proposal-document-template, dev, pro]
---
# Architecture Proposal Document Template

## Summary

**One-sentence:** Architecture Proposal Document Template: codified engineering practice that turns the recurring 'role-software-architect/Greenfield architecture proposal — concept to signed-off design pack' decision into a repeatable, auditable artefact.

**One-paragraph:** Architecture Proposal Document Template addresses the gap identified by the role-software-architect/Greenfield architecture proposal — concept to signed-off design pack playbook: Architects keep reinventing the proposal pack format; a tier-locked template (context, NFRs, options, scoring, ADR set, cost model, risks, decision) would be a strong pro-tier hook. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-software-architect/Greenfield architecture proposal — concept to signed-off design pack OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-software-architect/Greenfield architecture proposal — concept to signed-off design pack task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/software-developer` | parent role skill — provides the operating context for this methodology |

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
| `templates/architecture-proposal-document-template.json` | JSON schema for the Architecture Proposal Document Template output contract |
| `templates/architecture-proposal-document-template.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-architecture-proposal-document-template.py` | Enforce Architecture Proposal Document Template output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/dev/`
- upstream playbook: `role-software-architect/Greenfield architecture proposal — concept to signed-off design pack`
