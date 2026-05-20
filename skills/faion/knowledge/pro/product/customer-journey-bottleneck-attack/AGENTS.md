---
slug: customer-journey-bottleneck-attack
tier: pro
group: product
domain: product
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Customer Journey Bottleneck Attack: codified product practice that turns the recurring 'role-product-manager/Run a quarterly journey-bottleneck attack' decision into a repeatable, auditable artefact.
content_id: "57dc250eb3e7b93d"
tags: [customer-journey-bottleneck-attack, product, pro]
---
# Customer Journey Bottleneck Attack

## Summary

**One-sentence:** Customer Journey Bottleneck Attack: codified product practice that turns the recurring 'role-product-manager/Run a quarterly journey-bottleneck attack' decision into a repeatable, auditable artefact.

**One-paragraph:** Customer Journey Bottleneck Attack addresses the gap surfaced by 'role-product-manager/Run a quarterly journey-bottleneck attack'. Faion has continuous-discovery and OST but no journey-mapping methodology and no bottleneck-prioritization frame. This is the standard quarterly planning move in any mature product team and its absence pushes PMs back to feature-list roadmaps. Mechanism: typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of 'role-product-manager/Run a quarterly journey-bottleneck attack' OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is a greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)
- single-use throwaway task — overhead of the contract is not justified

## Prerequisites

- recent context for the 'role-product-manager/Run a quarterly journey-bottleneck attack' task (last 30 days of activity)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream
- baseline conventions documented (CLAUDE.md / AGENTS.md / CONVENTIONS.md)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/product/product-manager` | parent role skill — provides the operating context for this methodology |

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
| `templates/customer-journey-bottleneck-attack.json` | JSON schema for the Customer Journey Bottleneck Attack output contract |
| `templates/customer-journey-bottleneck-attack.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-customer-journey-bottleneck-attack.py` | Enforce Customer Journey Bottleneck Attack output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/product/product-manager/`
- upstream playbook: `role-product-manager/Run a quarterly journey-bottleneck attack`
- methodology family: `pro/product/` (gap-p2 batch, F-059-063)
