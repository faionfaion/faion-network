---
slug: sunset-vs-fold-framework
tier: pro
group: product
domain: product
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "ad4a5b2b4ce8c0f7"
summary: "Sunset Vs Fold Framework: produces a versioned, owner-signed artefact that closes the gap 'p3-technical-freelancer/Freelance-to-SaaS transition (6-month side build)'."
tags: [sunset-vs-fold-framework, product, pro]
---
# Sunset Vs Fold Framework

## Summary

**One-sentence:** Sunset Vs Fold Framework: produces a versioned, owner-signed artefact that closes the gap 'p3-technical-freelancer/Freelance-to-SaaS transition (6-month side build)'.

**One-paragraph:** Addresses the gap surfaced by 'p3-technical-freelancer/Freelance-to-SaaS transition (6-month side build)': If SaaS doesn't reach scale criteria, fold it into the freelance offer as a tool vs sunset — current product-lifecycle assumes a company can absorb a kill decision; solo can't. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a sunset vs fold framework artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'p3-technical-freelancer/Freelance-to-SaaS transition (6-month side build)' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working sunset vs fold framework artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'p3-technical-freelancer/Freelance-to-SaaS transition (6-month side build)' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/product/product` | parent domain group — provides operating context for Sunset Vs Fold Framework |

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
| `templates/sunset-vs-fold-framework.json` | JSON schema for the Sunset Vs Fold Framework output contract |
| `templates/sunset-vs-fold-framework.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-sunset-vs-fold-framework.py` | Enforce Sunset Vs Fold Framework output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/product/`
- upstream playbook: `p3-technical-freelancer/Freelance-to-SaaS transition (6-month side build)`
- pro/product/p3-technical-freelancer
