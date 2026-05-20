---
slug: architectural-impact-pr-ranking
tier: geek
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Architectural Impact Pr Ranking: codified engineering practice that turns the recurring 'p6-product-dev-team/Weekly architectural review (45 min)' decision into a repeatable, auditable artefact.
content_id: "6051b3752de5d84d"
tags: [architectural-impact-pr-ranking, dev, geek]
---
# Architectural Impact Pr Ranking

## Summary

**One-sentence:** Architectural Impact Pr Ranking: codified engineering practice that turns the recurring 'p6-product-dev-team/Weekly architectural review (45 min)' decision into a repeatable, auditable artefact.

**One-paragraph:** Architectural Impact Pr Ranking addresses the gap identified by the p6-product-dev-team/Weekly architectural review (45 min) playbook: Weekly arch review needs a deterministic way to surface high-impact PRs (touched files × layer crossings × public API delta). Currently architect picks by gut. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of p6-product-dev-team/Weekly architectural review (45 min) OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == geek or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the p6-product-dev-team/Weekly architectural review (45 min) task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/dev/software-developer` | parent role skill — provides the operating context for this methodology |

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
| `templates/architectural-impact-pr-ranking.json` | JSON schema for the Architectural Impact Pr Ranking output contract |
| `templates/architectural-impact-pr-ranking.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-architectural-impact-pr-ranking.py` | Enforce Architectural Impact Pr Ranking output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/dev/`
- upstream playbook: `p6-product-dev-team/Weekly architectural review (45 min)`
