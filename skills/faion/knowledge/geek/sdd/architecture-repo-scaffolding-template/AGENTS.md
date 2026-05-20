---
slug: architecture-repo-scaffolding-template
tier: geek
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Architecture Repo Scaffolding Template: codified spec-driven-development practice that turns the recurring 'role-software-architect/Architecture-as-code repository — continuous maintenance with monthly review' decision into a repeatable, auditable artefact.
content_id: "5bcf6d602e7bab4b"
tags: [architecture-repo-scaffolding-template, sdd, geek]
---
# Architecture Repo Scaffolding Template

## Summary

**One-sentence:** Architecture Repo Scaffolding Template: codified spec-driven-development practice that turns the recurring 'role-software-architect/Architecture-as-code repository — continuous maintenance with monthly review' decision into a repeatable, auditable artefact.

**One-paragraph:** Architecture Repo Scaffolding Template addresses the gap identified by the role-software-architect/Architecture-as-code repository — continuous maintenance with monthly review playbook: SDD covers spec / design / plan, but not the architect's repo structure (ADRs + diagrams + fitness functions + runbooks) as a first-class artifact. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-software-architect/Architecture-as-code repository — continuous maintenance with monthly review OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == geek or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-software-architect/Architecture-as-code repository — continuous maintenance with monthly review task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/sdd/sdd-author` | parent role skill — provides the operating context for this methodology |

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
| `templates/architecture-repo-scaffolding-template.json` | JSON schema for the Architecture Repo Scaffolding Template output contract |
| `templates/architecture-repo-scaffolding-template.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-architecture-repo-scaffolding-template.py` | Enforce Architecture Repo Scaffolding Template output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/sdd/`
- upstream playbook: `role-software-architect/Architecture-as-code repository — continuous maintenance with monthly review`
