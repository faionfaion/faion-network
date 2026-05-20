---
slug: async-standup-methodology
tier: solo
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Async Standup Methodology: codified delivery-management practice that turns the recurring 'role-project-manager/Async cross-timezone delivery cadence (P4 outsource)' decision into a repeatable, auditable artefact.
content_id: "bd542ca157a5c66c"
tags: [async-standup-methodology, pm, solo]
---
# Async Standup Methodology

## Summary

**One-sentence:** Async Standup Methodology: codified delivery-management practice that turns the recurring 'role-project-manager/Async cross-timezone delivery cadence (P4 outsource)' decision into a repeatable, auditable artefact.

**One-paragraph:** Async Standup Methodology addresses the gap identified by the role-project-manager/Async cross-timezone delivery cadence (P4 outsource) playbook: scrum-ceremonies assumes co-located sync standup. P4 outsource PMs with < 2h overlap need a written-first, bot-aggregated, AI-summarized format with explicit blocker-routing rules. agile-ceremonies-setup/standup-bot.yaml is a template fragment, not a methodology. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-project-manager/Async cross-timezone delivery cadence (P4 outsource) OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-project-manager/Async cross-timezone delivery cadence (P4 outsource) task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/pm/project-manager` | parent role skill — provides the operating context for this methodology |

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
| `templates/async-standup-methodology.json` | JSON schema for the Async Standup Methodology output contract |
| `templates/async-standup-methodology.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-async-standup-methodology.py` | Enforce Async Standup Methodology output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/pm/`
- upstream playbook: `role-project-manager/Async cross-timezone delivery cadence (P4 outsource)`
