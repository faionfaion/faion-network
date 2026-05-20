---
slug: ba-standup-script-template
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Ba Standup Script Template: codified business-analysis practice that turns the recurring 'role-business-analyst/Daily standup: BA-side prep + run' decision into a repeatable, auditable artefact.
content_id: "ef0406fb5e67a6a6"
tags: [ba-standup-script-template, ba, pro]
---
# Ba Standup Script Template

## Summary

**One-sentence:** Ba Standup Script Template: codified business-analysis practice that turns the recurring 'role-business-analyst/Daily standup: BA-side prep + run' decision into a repeatable, auditable artefact.

**One-paragraph:** Ba Standup Script Template addresses the gap identified by the role-business-analyst/Daily standup: BA-side prep + run playbook: BAs default to dev-style standup updates; a BA-specific 3-bullet script (clarifications / ACs ready / blockers) is a daily atomic unit. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-business-analyst/Daily standup: BA-side prep + run OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-business-analyst/Daily standup: BA-side prep + run task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/business-analyst` | parent role skill — provides the operating context for this methodology |

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
| `templates/ba-standup-script-template.json` | JSON schema for the Ba Standup Script Template output contract |
| `templates/ba-standup-script-template.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ba-standup-script-template.py` | Enforce Ba Standup Script Template output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/ba/`
- upstream playbook: `role-business-analyst/Daily standup: BA-side prep + run`
