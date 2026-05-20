---
slug: daily-ship-rubric
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Daily Ship Rubric: codified sdd practice that turns the recurring 'p1-solo-saas-builder/Daily SDD spec → vibe-code → review cycle' decision into a repeatable, auditable artefact.
content_id: "784d2d32b9dd4b9e"
tags: [daily-ship-rubric, sdd, solo]
---
# Daily Ship Rubric

## Summary

**One-sentence:** Daily Ship Rubric: codified sdd practice that turns the recurring 'p1-solo-saas-builder/Daily SDD spec → vibe-code → review cycle' decision into a repeatable, auditable artefact.

**One-paragraph:** Daily Ship Rubric addresses the gap surfaced by 'p1-solo-saas-builder/Daily SDD spec → vibe-code → review cycle'. What 'shipped today' means for a one-person SaaS; current quality-gates-confidence is generic. Mechanism: typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of 'p1-solo-saas-builder/Daily SDD spec → vibe-code → review cycle' OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is a greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)
- single-use throwaway task — overhead of the contract is not justified

## Prerequisites

- recent context for the 'p1-solo-saas-builder/Daily SDD spec → vibe-code → review cycle' task (last 30 days of activity)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream
- baseline conventions documented (CLAUDE.md / AGENTS.md / CONVENTIONS.md)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd` | parent role skill — provides the operating context for this methodology |

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
| `templates/daily-ship-rubric.json` | JSON schema for the Daily Ship Rubric output contract |
| `templates/daily-ship-rubric.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-daily-ship-rubric.py` | Enforce Daily Ship Rubric output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/sdd/sdd/`
- upstream playbook: `p1-solo-saas-builder/Daily SDD spec → vibe-code → review cycle`
- methodology family: `solo/sdd/` (gap-p2 batch, F-059-063)
