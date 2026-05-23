---
slug: retention-strategies
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Catalog of 6 retention loop archetypes + 4 engagement mechanics + a re-engagement campaign playbook — picked by product fit, not stacked simultaneously.
content_id: "6ec95232710a597b"
complexity: deep
produces: playbook-step
est_tokens: 4200
tags: [retention, loops, engagement, streaks, re-engagement]
---
# Retention Strategies

## Summary

**One-sentence:** Catalog of 6 retention loop archetypes + 4 engagement mechanics + a re-engagement campaign playbook — picked by product fit, not stacked simultaneously.

**One-paragraph:** Catalog of 6 retention loop archetypes + 4 engagement mechanics + a re-engagement campaign playbook — picked by product fit, not stacked simultaneously. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

**Ефективно для:**

- Product teams що мають baseline retention measured і шукають lifts.
- Перед quarterly product roadmap — pick loop архетип як north-star feature theme.
- При перейті з growth (acquisition) до retention focus.
- Існуюча engagement mechanic underperform — pick новий замість stacking.

## Applies If (ALL must hold)

- retention-metrics уже виконано — locked formulas + >= 90 days data.
- Product має > 1 active feature category — є де loop wire.
- Team здатна на quarterly feature build (>= 1 engineer + designer).

## Skip If (ANY kills it)

- Retention baseline не виміряний — спершу retention-metrics.
- Single-feature product без сurface для loop — stacking forced.
- Engineering capacity = 0 — це feature investment, не configuration.

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
| `pro/marketing/growth-marketer` | Parent role context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
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
| `templates/playbook-step-skeleton.md` | Retention Strategies skeleton — fill per artefact, do not commit free-form output. |
| `templates/_smoke-test.md` | Minimum viable filled-in Retention Strategies. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-retention-strategies.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[retention-metrics]]
- [[ops-churn-basics]]
- [[ops-churn-prevention]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
