---
slug: from-hourly-to-fixed-transition
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: 12-week three-phase transition off hourly billing: convert highest-margin client first, hold 2-3 overlap clients, productize one SKU, single-round re-price, 6-8 week cash bridge.
content_id: "0fc19fe7bbd006ab"
complexity: deep
produces: spec
est_tokens: 4200
tags: [pricing, freelance, productized, transition, retainer, cash-flow]
---
# From Hourly to Fixed-Price Transition

## Summary

**One-sentence:** 12-week three-phase transition off hourly billing: convert highest-margin client first, hold 2-3 overlap clients, productize one SKU, single-round re-price, 6-8 week cash bridge.

**One-paragraph:** 12-week three-phase transition off hourly billing: convert highest-margin client first, hold 2-3 overlap clients, productize one SKU, single-round re-price, 6-8 week cash bridge. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

**Ефективно для:**

- Freelancers / studios що шукають escape з hourly trap без revenue collapse.
- Перед запуском productized SKU — це pre-work плану.
- Якщо effective hourly < $150 і ставка stuck, transition окуповується.
- При зростанні до 5+ clients — hourly admin overhead починає вбивати margin.

## Applies If (ALL must hold)

- Active book >= 3 paying hourly clients з документованими hours per client.
- Founder здатний особисто провести цикл re-pricing conversations.
- Savings + credit + signed pipeline складають >= 6 weeks of monthly burn (cash bridge).

## Skip If (ANY kills it)

- Cash bridge < 6 weeks — transition collapses pre-finish; fix bridge first.
- < 3 paying clients — занадто мало data для productize one repeatable scope.
- Already 80%+ fixed-price — це formalisation problem, не transition.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Versioned space for the artefact | Git repo / wiki with history | team |
| Named owner | Person + role | team / RACI |
| Trigger event | Event / threshold / schedule | operating cadence |
| Upstream methodologies in `Assumes Loaded` | Already routine for the role | team training |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/gtm-strategist` | Parent role context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/05-examples.xml` | medium | One worked end-to-end example | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-artefact` | haiku | Template fill from header + section list. |
| `draft-rationale` | sonnet | Per-decision rationale + rejected alternatives. |
| `review-tradeoffs` | opus | Cross-decision synthesis + reversibility judgment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec-skeleton.md` | From Hourly to Fixed-Price Transition skeleton — fill per artefact, do not commit free-form output. |
| `templates/_smoke-test.md` | Minimum viable filled-in From Hourly to Fixed-Price Transition. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-from-hourly-to-fixed-transition.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[agency-proposal-template-system]]
- [[agency-pricing-tiers]]
- [[agency-niche-positioning]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
