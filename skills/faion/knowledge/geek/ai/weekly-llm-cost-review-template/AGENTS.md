---
slug: weekly-llm-cost-review-template
tier: geek
group: ai
domain: ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "6f7427fc866d90ce"
summary: "Weekly Llm Cost Review Template: produces a versioned, owner-signed artefact that closes the gap 'role-ml-engineer/Weekly model-cost + token-budget review'."
tags: [weekly-llm-cost-review-template, ai, geek]
---
# Weekly Llm Cost Review Template

## Summary

**One-sentence:** Weekly Llm Cost Review Template: produces a versioned, owner-signed artefact that closes the gap 'role-ml-engineer/Weekly model-cost + token-budget review'.

**One-paragraph:** Addresses the gap surfaced by 'role-ml-engineer/Weekly model-cost + token-budget review': cost-optimization + llm-cost-basics exist but there is no cadence template for the weekly review with concrete pivots and decision log. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a weekly llm cost review template artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'role-ml-engineer/Weekly model-cost + token-budget review' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == geek or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working weekly llm cost review template artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'role-ml-engineer/Weekly model-cost + token-budget review' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai` | parent domain group — provides operating context for Weekly Llm Cost Review Template |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules grounded in the cited gap | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/weekly-llm-cost-review-template.json` | JSON schema for the Weekly Llm Cost Review Template output contract |
| `templates/weekly-llm-cost-review-template.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-weekly-llm-cost-review-template.py` | Enforce Weekly Llm Cost Review Template output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/ai/`
- upstream playbook: `role-ml-engineer/Weekly model-cost + token-budget review`
- geek/ai/role-ml-engineer
