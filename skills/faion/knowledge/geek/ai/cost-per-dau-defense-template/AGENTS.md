---
slug: cost-per-dau-defense-template
tier: geek
group: ai
domain: ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Cost Per Dau Defense Template: codified ai practice that turns the recurring 'role-ml-engineer/Production inference cost optimization sweep' decision into a repeatable, auditable artefact.
content_id: "f1101cbaba0f9374"
tags: [cost-per-dau-defense-template, ai, geek]
---
# Cost Per Dau Defense Template

## Summary

**One-sentence:** Cost Per Dau Defense Template: codified ai practice that turns the recurring 'role-ml-engineer/Production inference cost optimization sweep' decision into a repeatable, auditable artefact.

**One-paragraph:** Cost Per Dau Defense Template addresses the gap surfaced by 'role-ml-engineer/Production inference cost optimization sweep'. How an ML engineer presents and defends an AI unit-economics number to finance / leadership. Bridges ml-engineering and finops. Mechanism: typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of 'role-ml-engineer/Production inference cost optimization sweep' OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == geek or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is a greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)
- single-use throwaway task — overhead of the contract is not justified

## Prerequisites

- recent context for the 'role-ml-engineer/Production inference cost optimization sweep' task (last 30 days of activity)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream
- baseline conventions documented (CLAUDE.md / AGENTS.md / CONVENTIONS.md)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer` | parent role skill — provides the operating context for this methodology |

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
| `templates/cost-per-dau-defense-template.json` | JSON schema for the Cost Per Dau Defense Template output contract |
| `templates/cost-per-dau-defense-template.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cost-per-dau-defense-template.py` | Enforce Cost Per Dau Defense Template output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/ai/ml-engineer/`
- upstream playbook: `role-ml-engineer/Production inference cost optimization sweep`
- methodology family: `geek/ai/` (gap-p2 batch, F-059-063)
