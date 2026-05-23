---
slug: growth-brand-positioning
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Six-step positioning spec: define precise customer + map alternatives + name single 'only we' differentiator + pick category + craft statement + validate via customer interviews.
content_id: "d0e363807b489bb3"
complexity: deep
produces: spec
est_tokens: 4200
tags: [positioning, brand, marketing, differentiation, gtm]
---
# Brand Positioning

## Summary

**One-sentence:** Six-step positioning spec: define precise customer + map alternatives + name single 'only we' differentiator + pick category + craft statement + validate via customer interviews.

**One-paragraph:** Six-step positioning spec: define precise customer + map alternatives + name single 'only we' differentiator + pick category + craft statement + validate via customer interviews. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

**Ефективно для:**

- Перед запуском GTM strategy — positioning є upstream.
- Product чує 'мы как X, тільки cheaper / faster' — це pricing проблема + positioning crime.
- Founder каже 'we serve everyone' — це anti-positioning, fix first.
- Перед website rebuild / sales page sprint — anchor у positioning спершу.

## Applies If (ALL must hold)

- Product has paying customers + identifiable winners (avatar candidates).
- Команда здатна на 10+ customer interviews protect quarter.
- Founder accepts narrowing — pre-committed до exclusion of 'serve everyone' wording.

## Skip If (ANY kills it)

- Pre-product / 0 paying customers — speculate, не position.
- Founder unwilling narrow — positioning fail under pressure.
- Single-vertical product with > 90% revenue from one segment — formalize, не re-position.

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
| `templates/spec-skeleton.md` | Brand Positioning skeleton — fill per artefact, do not commit free-form output. |
| `templates/_smoke-test.md` | Minimum viable filled-in Brand Positioning. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-growth-brand-positioning.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[growth-gtm-strategy]]
- [[agency-niche-positioning]]
- [[growth-press-coverage]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
