---
slug: client-maturity-assessment-rubric
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Client Maturity Assessment Rubric: codified pm practice that turns the recurring 'role-project-manager/Client onboarding into our delivery cadence (two weeks)' decision into a repeatable, auditable artefact.
content_id: "923a8f5bf530bfd1"
tags: [client-maturity-assessment-rubric, pm, pro]
---
# Client Maturity Assessment Rubric

## Summary

**One-sentence:** Client Maturity Assessment Rubric: codified pm practice that turns the recurring 'role-project-manager/Client onboarding into our delivery cadence (two weeks)' decision into a repeatable, auditable artefact.

**One-paragraph:** Client Maturity Assessment Rubric addresses the gap surfaced by 'role-project-manager/Client onboarding into our delivery cadence (two weeks)'. Client onboarding success is dominated by how mature/agile-fluent the client is, but no rubric exists. PMs guess and over- or under-engineer the cadence. Mechanism: typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of 'role-project-manager/Client onboarding into our delivery cadence (two weeks)' OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is a greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)
- single-use throwaway task — overhead of the contract is not justified

## Prerequisites

- recent context for the 'role-project-manager/Client onboarding into our delivery cadence (two weeks)' task (last 30 days of activity)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream
- baseline conventions documented (CLAUDE.md / AGENTS.md / CONVENTIONS.md)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/project-manager` | parent role skill — provides the operating context for this methodology |

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
| `synthesize_decision` | sonnet | Per-instance judgment with bounded inputs |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/client-maturity-assessment-rubric.json` | JSON schema for the Client Maturity Assessment Rubric output contract |
| `templates/client-maturity-assessment-rubric.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-client-maturity-assessment-rubric.py` | Enforce Client Maturity Assessment Rubric output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/pm/project-manager/`
- upstream playbook: `role-project-manager/Client onboarding into our delivery cadence (two weeks)`
- methodology family: `pro/pm/` (gap-p2 batch, F-059-063)
