---
slug: coverage-rebuild-playbook
tier: solo
group: testing
domain: testing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Coverage Rebuild Playbook: codified testing practice that turns the recurring 'role-software-developer/Test-coverage rebuild from 30% to 70% (6 weeks)' decision into a repeatable, auditable artefact.
content_id: "940c9a02ce3660b6"
tags: [coverage-rebuild-playbook, testing, solo]
---
# Coverage Rebuild Playbook

## Summary

**One-sentence:** Coverage Rebuild Playbook: codified testing practice that turns the recurring 'role-software-developer/Test-coverage rebuild from 30% to 70% (6 weeks)' decision into a repeatable, auditable artefact.

**One-paragraph:** Coverage Rebuild Playbook addresses the gap surfaced by 'role-software-developer/Test-coverage rebuild from 30% to 70% (6 weeks)'. Existing testing methodologies cover frameworks but not the multi-week project of raising coverage on an existing low-coverage codebase. Mechanism: typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of 'role-software-developer/Test-coverage rebuild from 30% to 70% (6 weeks)' OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is a greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)
- single-use throwaway task — overhead of the contract is not justified

## Prerequisites

- recent context for the 'role-software-developer/Test-coverage rebuild from 30% to 70% (6 weeks)' task (last 30 days of activity)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream
- baseline conventions documented (CLAUDE.md / AGENTS.md / CONVENTIONS.md)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/testing/` | parent group — provides the operating context for this methodology |

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
| `templates/coverage-rebuild-playbook.json` | JSON schema for the Coverage Rebuild Playbook output contract |
| `templates/coverage-rebuild-playbook.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-coverage-rebuild-playbook.py` | Enforce Coverage Rebuild Playbook output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/testing/`
- upstream playbook: `role-software-developer/Test-coverage rebuild from 30% to 70% (6 weeks)`
- methodology family: `solo/testing/` (gap-p2 batch, F-059-063)
