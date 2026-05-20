---
slug: daily-marketing-standup-checklist
tier: free
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Daily Marketing Standup Checklist: codified marketing practice that turns the recurring 'role-growth-marketing/Daily 15-min content + social pulse check' decision into a repeatable, auditable artefact.
content_id: "0678d769b9344680"
tags: [daily-marketing-standup-checklist, marketing, free]
---
# Daily Marketing Standup Checklist

## Summary

**One-sentence:** Daily Marketing Standup Checklist: codified marketing practice that turns the recurring 'role-growth-marketing/Daily 15-min content + social pulse check' decision into a repeatable, auditable artefact.

**One-paragraph:** Daily Marketing Standup Checklist addresses the gap surfaced by 'role-growth-marketing/Daily 15-min content + social pulse check'. P6 in-house marketers and P4 solo growth folks both lack a single-screen morning routine; reduces tool-sprawl pain by forcing one consolidated check. Mechanism: typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of 'role-growth-marketing/Daily 15-min content + social pulse check' OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == free or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is a greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)
- single-use throwaway task — overhead of the contract is not justified

## Prerequisites

- recent context for the 'role-growth-marketing/Daily 15-min content + social pulse check' task (last 30 days of activity)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream
- baseline conventions documented (CLAUDE.md / AGENTS.md / CONVENTIONS.md)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `free/marketing/marketing-manager` | parent role skill — provides the operating context for this methodology |

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
| `templates/daily-marketing-standup-checklist.json` | JSON schema for the Daily Marketing Standup Checklist output contract |
| `templates/daily-marketing-standup-checklist.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-daily-marketing-standup-checklist.py` | Enforce Daily Marketing Standup Checklist output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `free/marketing/marketing-manager/`
- upstream playbook: `role-growth-marketing/Daily 15-min content + social pulse check`
- methodology family: `free/marketing/` (gap-p2 batch, F-059-063)
