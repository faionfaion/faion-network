---
slug: per-client-credential-isolation-pattern
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Per Client Credential Isolation Pattern: codified infra practice that turns the recurring 'p4-outsource-specialist/New-project machine setup (laptop + desktop)' decision into a repeatable, auditable artefact.
content_id: "4195343757949f2e"
tags: [per-client-credential-isolation-pattern, infra, pro]
---
# Per Client Credential Isolation Pattern

## Summary

**One-sentence:** Per Client Credential Isolation Pattern: codified infra practice that turns the recurring 'p4-outsource-specialist/New-project machine setup (laptop + desktop)' decision into a repeatable, auditable artefact.

**One-paragraph:** Per Client Credential Isolation Pattern addresses the gap identified by the p4-outsource-specialist/New-project machine setup (laptop + desktop) playbook: Outsource specialist juggles 1-3 clients with strict no-cross-leakage rules. No faion methodology covers per-client SSH/GPG/cloud credential separation pattern. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of p4-outsource-specialist/New-project machine setup (laptop + desktop) OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the p4-outsource-specialist/New-project machine setup (laptop + desktop) task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer` | parent role skill — provides the operating context for this methodology |

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
| `templates/per-client-credential-isolation-pattern.json` | JSON schema for the Per Client Credential Isolation Pattern output contract |
| `templates/per-client-credential-isolation-pattern.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-per-client-credential-isolation-pattern.py` | Enforce Per Client Credential Isolation Pattern output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/infra/devops-engineer/`
- upstream playbook: `p4-outsource-specialist/New-project machine setup (laptop + desktop)`
